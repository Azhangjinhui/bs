from pyspark.sql.types import StructType, StructField, StringType, DecimalType, IntegerType, ArrayType
import os
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql import SparkSession

# 设置环境变量
os.environ['JAVA_HOME'] = '/usr/local/jdk1.8.0_281/'
os.environ['SPARK_HOME'] = '/usr/local/spark'

spark = SparkSession.builder \
	.appName("KafkaStreamReader") \
	.master("local[2]") \
	.config("spark.sql.shuffle.partitions", 4) \
	.config("spark.jars", "/usr/local/spark/jars/spark-doris-connector-spark-3.5-25.1.0.jar") \
	.getOrCreate()

schema = StructType([
	StructField("data", ArrayType(StructType([
		StructField("province", StringType(), False),
		StructField("co2_mt", StringType(), False),
		StructField("sector", StringType(), False),
		StructField("year", StringType(), False)
	])), False)
])
# 批处理方式读取Kafka数据（非流处理）
df = spark.read \
	.format("kafka") \
	.option("kafka.bootstrap.servers", "node01:9092,node02:9092") \
	.option("subscribe", "carbon_china_provincial_carbon_2024") \
	.option("startingOffsets", "earliest") \
	.option("endingOffsets", "latest") \
	.load() \
	.select(from_json(col("value").cast("string"), schema).alias("root")) \
	.select(explode(col("root.data")).alias("d")) \
	.select(
	col("d.province"),
	col("d.co2_mt").cast(DecimalType(15,6)).alias('co2_mt'),
	col("d.sector"),
	col("d.year").cast(IntegerType()).alias('year')
)


df.write.format("doris") \
	.option("doris.table.identifier", "carbon.ods_china_provincial_carbon_2024") \
	.option("doris.fenodes", "node01:8030") \
	.option("doris.query.port", "9030") \
	.option("user", "root") \
	.option("password", "") \
	.option("doris.write.fields", "province,co2_mt,sector,year") \
	.option("doris.sink.batch.size", "10") \
	.option("doris.sink.max-retries", "1") \
	.mode("overwrite") \
	.save()

spark.stop()
