import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# 设置环境变量
os.environ['JAVA_HOME'] = '/usr/local/jdk1.8.0_281/'
os.environ['SPARK_HOME'] = '/usr/local/spark'

# 1. 构建省份映射字典
province_mapping = {
	"Shanghai": "上海",
	"Yunnan": "云南",
	"Inner Mongolia": "内蒙古",
	"Beijing": "北京",
	"Jilin": "吉林",
	"Sichuan": "四川",
	"Tianjin": "天津",
	"Ningxia": "宁夏",
	"Anhui": "安徽",
	"Shandong": "山东",
	"Shanxi": "山西",
	"Guangdong": "广东",
	"Guangxi": "广西",
	"Xinjiang": "新疆",
	"Jiangsu": "江苏",
	"Jiangxi": "江西",
	"Hebei": "河北",
	"Henan": "河南",
	"Zhejiang": "浙江",
	"Hainan": "海南",
	"Hubei": "湖北",
	"Hunan": "湖南",
	"Gansu": "甘肃",
	"Fujian": "福建",
	"Tibet": "西藏",
	"Guizhou": "贵州",
	"Liaoning": "辽宁",
	"Chongqing": "重庆",
	"Shaanxi": "陕西",
	"Qinghai": "青海",
	"Heilongjiang": "黑龙江"
}

def convert_province(province_pinyin):
	return province_mapping.get(province_pinyin, province_pinyin)  # 处理未匹配情况
convert_province_udf = udf(convert_province, StringType())
spark = SparkSession.builder \
	.appName("dorisReadWrite") \
	.master("local[2]") \
	.config("spark.sql.shuffle.partitions", 4) \
	.config("spark.jars", "/usr/local/spark/jars/spark-doris-connector-spark-3.5-25.1.0.jar") \
	.getOrCreate()
dorisSparkDF = spark.read.format("doris") \
	.option("doris.table.identifier", "carbon.ods_china_provincial_carbon_2024") \
	.option("doris.fenodes", "node01:8030") \
	.option("doris.query.port", "9030") \
	.option("user", "root") \
	.option("password", "") \
	.load()

dorisSparkDF.createOrReplaceTempView("ods_china_provincial_carbon_2024")

df = spark.sql("""
               select province, co2_mt, sector, year
               from ods_china_provincial_carbon_2024
               where year=2024 and sector='Total'
               """)

df = df.withColumn("province", convert_province_udf(df["province"]))

df.show()
df.write.format("doris") \
	.option("doris.table.identifier", "dwd_carbon.dwd_china_provincial_total_carbon_2024") \
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