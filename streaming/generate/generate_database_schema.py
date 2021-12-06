from typing import List

from sqlalchemy.engine import Inspector

from constants.constants import MAP_SQLALCHEMY_TYPE_TO_SPARK_SQL_TYPE


def get_schema_table(inspector: Inspector, table_name: str):
    columns = []
    for column in inspector.get_columns(table_name):
        columns.append(column)
    return to_string_structure_type(columns)


def sqlalchemy_to_spark(sqlalchemy_type: str):
    for key in MAP_SQLALCHEMY_TYPE_TO_SPARK_SQL_TYPE.keys():
        if key in sqlalchemy_type:
            return MAP_SQLALCHEMY_TYPE_TO_SPARK_SQL_TYPE[key]
    return None


def to_string_structure_type(columns: List[dict]) -> str:
    res = 'StructType([\n'
    for column in columns:
        spark_type = sqlalchemy_to_spark(str(column.get('type')))
        res += 'StructField("' + column.get('name') + '", ' + spark_type + '()),\n'
    res += '])'
    return res


def get_list_column_of_table(inspector: Inspector, table_name: str):
    columns = []
    for column in inspector.get_columns(table_name):
        columns.append(column['name'])
    return columns
