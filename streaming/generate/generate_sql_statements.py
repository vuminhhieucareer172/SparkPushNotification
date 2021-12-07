import sqlparse
from sqlalchemy.engine import Inspector

from streaming.generate.generate_database_schema import get_list_column_of_table


def format_sql_spark(sql: str, inspector: Inspector):
    parsed = sqlparse.parse(sql)
    select_value = ''
    i = 0
    list_tables = []
    while i < len(parsed[0].tokens):
        if parsed[0].tokens[i].value.upper() == 'SELECT':
            i += 2
            select_value = parsed[0].tokens[i].value
        if parsed[0].tokens[i].value.upper() == 'FROM':
            i += 2
            list_tables = parsed[0].tokens[i].value.split(', ')
            if select_value == '*':
                list_cols = []
                for table1 in list_tables:
                    cols = get_list_column_of_table(inspector=inspector, table_name=table1)
                    cols = list(map(lambda col: table1 + '.' + col + ' as ' + table1 + '_' + col, cols))
                    list_cols = list_cols + cols
                sql = sql.replace('*', ', '.join(list_cols))
        if parsed[0].tokens[i].value.upper() == 'GROUP BY':
            if select_value == '*':
                list_cols = []
                for table1 in list_tables:
                    cols = get_list_column_of_table(inspector=inspector, table_name=table1)
                    cols = list(map(lambda col: table1 + '.' + col, cols))
                    list_cols = list_cols + cols
                sql = sql.replace(parsed[0].tokens[i].value + ' ' + parsed[0].tokens[i+2].value,
                                  f"{parsed[0].tokens[i].value.upper() + ' ' + parsed[0].tokens[i+2].value}{', ' + ', '.join(list_cols) if list_cols else ''}")
        i += 1
    return sql
