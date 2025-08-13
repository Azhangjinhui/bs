import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

# 设置环境变量
os.environ['JAVA_HOME'] = '/usr/local/jdk1.8.0_281/'
os.environ['SPARK_HOME'] = '/usr/local/spark'


sector_mapping={
	'Power':'电力',
	'Ground Transport':'地面运输',
	'Industry':'工业',
	'Residential':'居民消费',
	'Domestic Aviation':'国内航空',
	'International Aviation':'国际航空'

}

spark = SparkSession.builder \
	.appName("dorisRead") \
	.master("local[2]") \
	.config("spark.sql.shuffle.partitions", 4) \
	.config("spark.jars", "/usr/local/spark/jars/spark-doris-connector-spark-3.5-25.1.0.jar") \
	.getOrCreate()

dorisSparkDF = spark.read.format("doris") \
	.option("doris.table.identifier", "carbon.ods_all_country_carbon_2019_2024") \
	.option("doris.fenodes", "node01:8030") \
	.option("doris.query.port", "9030") \
	.option("user", "root") \
	.option("password", "") \
	.load()

dorisSparkDF.createOrReplaceTempView("ods_all_country_carbon_2019_2024")
df = spark.sql("""
               select area,co2_mt,sector,year from ods_all_country_carbon_2019_2024
               where  area='China' and sector !='Total'
               """)
@udf(returnType=StringType())
def convert_sector(sector_en):
	return sector_mapping.get(sector_en, sector_en)
df=df.withColumn('sector',convert_sector(df['sector']))
df.show()

df.write.format("doris") \
	.option("doris.table.identifier", "dwd_carbon.dwd_china_carbon_sector_2024") \
	.option("doris.fenodes", "node01:8030") \
	.option("doris.query.port", "9030") \
	.option("user", "root") \
	.option("password", "") \
	.option("doris.write.fields", "area,co2_mt,sector,year") \
	.option("doris.sink.batch.size", "10") \
	.option("doris.sink.max-retries", "1") \
	.mode("overwrite") \
	.save()
spark.stop()