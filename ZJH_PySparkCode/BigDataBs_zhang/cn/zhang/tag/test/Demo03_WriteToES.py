from pyspark.sql import SparkSession
import os

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	Demo03_WriteToES
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

# 构建SparkSession
# 建造者模式：类名.builder.配置…….getOrCreate()
# 自动帮你构建一个SparkSession对象，只要指定你需要哪些配置就可
spark = SparkSession \
	.builder \
	.master("local[2]") \
	.appName("SparkSQLAppName") \
	.config("spark.sql.shuffle.partitions", 4) \
	.config("hive.metastore.uris","thrift://up01:9083") \
	.config("hive.metastore.warehouse.dir","hdfs://up01:8020/user/hive/warehouse") \
	.enableHiveSupport() \
	.getOrCreate()
input_df = spark.read.table("default.tb_hdfs")
input_df.printSchema()
input_df.show()

input_df.write.format('es').option('es.resource','test_spark_write_es').option('es.nodes','up01:9200').option("es.mapping.id","id").save()
# 关闭SparkSession
spark.stop()
