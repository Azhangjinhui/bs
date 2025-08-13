import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

# 设置环境变量
os.environ['JAVA_HOME'] = '/usr/local/jdk1.8.0_281/'
os.environ['SPARK_HOME'] = '/usr/local/spark'



area_mapping={
	'America':'美国',
	'China':'中国',
	'England': '英国',
	'France':'法国',
	'Germany':'德国',
	'India':'印度',
	'Italy':'意大利',
	'Japan':'日本',
	'Russia':'俄罗斯',
	'WORLD':'全球'

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
               select area, co2_mt, sector, year
               from ods_all_country_carbon_2019_2024
               where sector = 'Total'
                 and area in ('China', 'England', 'Germany', 'Russia', 'America','WORLD')
               """)

@udf(returnType=StringType())
def convert_area(area_en):
	return area_mapping.get(area_en, area_en)
df=df.withColumn('area',convert_area(df['area']))

df.show()
df.write.format("doris") \
	.option("doris.table.identifier", "dwd_carbon.dwd_five_country_Total_carbon_2019_2024") \
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