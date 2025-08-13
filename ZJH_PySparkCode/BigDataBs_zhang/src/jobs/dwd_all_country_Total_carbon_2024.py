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
area_mapping={
	'America':'美国',
	'China':'中国',
	'England': '英国',
	'France':'法国',
	'Germany':'德国',
	'India':'印度',
	'Italy':'意大利',
	'Japan':'日本',
	'Russia':'俄罗斯'

}
country_lat_lon = {
	"中国": (116.4074, 39.9042),  # 北京：经度116.4074，纬度39.9042
	"美国": (-74.0060, 40.7128),  # 纽约
	"英国": (-0.1278, 51.5074),   # 伦敦
	"法国": (2.3522, 48.8566),    # 巴黎
	"德国": (13.4050, 52.5200),   # 柏林
	"印度": (77.2090, 28.6139),   # 新德里
	"意大利": (12.4964, 41.9028), # 罗马
	"日本": (139.6917, 35.6895),  # 东京
	"俄罗斯": (37.6173, 55.7558)  # 莫斯科
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
               where year=2024 and sector ='Total' and area !='WORLD'
               """)
@udf(returnType=StringType())
def convert_sector(sector_en):
	return sector_mapping.get(sector_en, sector_en)
df=df.withColumn('sector',convert_sector(df['sector']))
@udf(returnType=StringType())
def convert_area(area_en):
	return area_mapping.get(area_en, area_en)
df=df.withColumn('area',convert_area(df['area']))
@udf(returnType=StringType())
def get_longitude(country):
	return str(country_lat_lon.get(country, (None, None))[0])
@udf(returnType=StringType())
def get_latitude(country):
	return str(country_lat_lon.get(country, (None, None))[1])
df = df.withColumn("longitude", get_longitude(df["area"]))
df = df.withColumn("latitude", get_latitude(df["area"]))

df.show()
df.write.format("doris") \
	.option("doris.table.identifier", "dwd_carbon.dwd_all_country_Total_carbon_2024") \
	.option("doris.fenodes", "node01:8030") \
	.option("doris.query.port", "9030") \
	.option("user", "root") \
	.option("password", "") \
	.option("doris.write.fields", "area,co2_mt,sector,year,longitude,latitude") \
	.option("doris.sink.batch.size", "10") \
	.option("doris.sink.max-retries", "1") \
	.mode("overwrite") \
	.save()
spark.stop()