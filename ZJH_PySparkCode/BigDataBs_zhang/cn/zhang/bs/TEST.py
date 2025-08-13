from pyspark.sql import SparkSession
import os

os.environ['JAVA_HOME'] = '/usr/local/jdk1.8.0_281/'
os.environ['SPARK_HOME'] = '/usr/local/spark'



spark = SparkSession.builder \
	.appName("KafkaStreamReader") \
	.master("local[2]") \
	.config("spark.sql.shuffle.partitions", 4) \
	.getOrCreate()

# 后续代码保持不变
df = spark.readStream \
	.format("kafka") \
	.option("kafka.bootstrap.servers", "node01:9092,node02:9092") \
	.option("subscribe", "test2") \
	.option("startingOffsets", "earliest") \
	.load()

df = df.selectExpr("cast(value as string)")

query = df.writeStream \
	.outputMode("append") \
	.format("console") \
	.start()

query.awaitTermination()