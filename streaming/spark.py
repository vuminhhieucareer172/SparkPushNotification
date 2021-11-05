import subprocess

from pyspark import SparkConf, SparkContext, SQLContext
from starlette import status
from starlette.responses import JSONResponse

from backend.utils.util_get_config import get_config
from constants.constants import CONFIG_SPARK
from database.db import DB


class Spark:
    """ A singleton backbone for Spark Creation"""

    class Internal:
        """ Implementation of the singleton interface """

        def __init__(self):
            print("starting spark")
            app_name = "DB streaming"
            master = "local[10]"
            job_streaming_properties = get_config(CONFIG_SPARK)
            if job_streaming_properties is None:
                print("missing job streaming config, using default params")
                self.conf = SparkConf().setAppName(app_name) \
                    .set("spark.sql.execution.arrow.pyspark.enabled", "true") \
                    .set("spark.sql.legacy.timeParserPolicy", "LEGACY")
                self.sc = SparkContext(master=master, conf=self.conf).getOrCreate()
                self.sql_context = SQLContext(self.sc)
            else:
                try:
                    self.conf = SparkConf().setAppName(job_streaming_properties.value.get('name_job', app_name))
                    self.sc = SparkContext(master=job_streaming_properties.value.get('master', master), conf=self.conf)\
                        .getOrCreate()
                    self.sql_context = SQLContext(self.sc)
                except Exception as e:
                    print(e)
                    raise ValueError(str(e))
            print(f"started spark application with name {app_name}")

        def get_instance(self) -> SparkContext:
            """ instance retrieval method, return spark sql context """
            return self.sc

        def get_sql_context(self) -> SQLContext:
            """ instance retrieval method, return sql context for dataframes """
            return self.sql_context

    __spark_instance = None
    __spark_job_pid = None

    def __init__(self):
        """ Create singleton Spark instance """

        if Spark.__spark_instance is None:
            Spark.__spark_instance = Spark.Internal()

        self.__dict__['SparkInstance'] = Spark.__spark_instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__spark_instance, attr)

    def get_pid(self):
        """ Return running job pid """
        return self.__spark_job_pid

    def submit_job_spark(self, file: str):
        """ Submit a job from file python to spark cluster """
        cmd = "nohup", "spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2", \
              "streaming/job_stream/job/" + file + ".py"
        proc = subprocess.Popen(cmd)
        self.__spark_job_pid = proc.pid
        return proc


def status_spark(db: DB):
    try:
        spark_instance = Spark().get_instance()
        is_stopped = spark_instance._jsc.sc().isStopped()
        if not is_stopped:
            return JSONResponse(content={"message": "running"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "stopped"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "stopped"}, status_code=status.HTTP_400_BAD_REQUEST)
