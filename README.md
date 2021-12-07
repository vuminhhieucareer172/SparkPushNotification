# Database streaming


## Prerequisites & Documentation

Make sure to install enough requirements before continue. All requirements are listed below:

* Operating systems: Linux, macOS
* Python version >= 3.6
* [Spark 3.x](https://spark.apache.org/downloads.html) & [docs](https://spark.apache.org/docs/latest/)
* [Kafka 2.x](https://kafka.apache.org/quickstart) & [docs](https://kafka.apache.org/documentation/)
* Mysql(<=5.7)/PostgreSQL/SQL server
* Npm, nodejs

## Install

- Frontend:

```
    npm install -g @angular/cli && npm install
```

- Backend:

    * Install package for system corresponding to sql service:
      * For [MySQL](https://pypi.org/project/mysqlclient/) /PostgreSQL
      * For [SQL server](https://github.com/mkleehammer/pyodbc/wiki/Install)

    * Install package python:
        
```
        pip3 install -r requirements.txt
```

## Usage
### Start frontend

    ng serve

### Start backend

    ./run_api.sh

### Upgrade database (make sure .env is configured)

    ./upgrade_db.sh


## Option (should read)

- If you want to have some queries group by not full field in table, please execute this command in super privilege:


    SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

