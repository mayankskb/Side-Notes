import subprocess as sp
from pyspark.sql import SparkSession

#Running a .sh file
sp.call(['./bash.sh'], shell = True)

sp.run(['hadoop', 'fs', '-put','test.csv','/mayank/'])
spark = SparkSession.builder.appName('file dataframe poc').getOrCreate()

# Read from HDFS
df_load = spark.read.csv('hdfs://localhost:9000/mayank/*.csv')
df_load.show()


sp.run(['hadoop', 'fs', '-mv','/mayank/*.csv','/moved'])
