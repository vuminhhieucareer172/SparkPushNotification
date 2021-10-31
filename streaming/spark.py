import subprocess

from pyspark import SparkConf, SparkContext, SQLContext


class Spark:
    """ A singleton backbone for Spark Creation"""

    class Internal:
        """ Implementation of the singleton interface """

        def __init__(self):
            app_name = "Job Alert Yourway"
            print("starting spark")

            self.conf = SparkConf().setAppName(app_name) \
                .set("spark.sql.execution.arrow.pyspark.enabled", "true") \
                .set("spark.sql.legacy.timeParserPolicy", "LEGACY")
            self.sc = SparkContext(master='local[10]', conf=self.conf).getOrCreate()
            self.sql_context = SQLContext(self.sc)

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
