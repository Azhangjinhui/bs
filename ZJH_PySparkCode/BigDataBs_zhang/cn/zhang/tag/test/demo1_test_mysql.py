from pyspark.sql import SparkSession
import os

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	demo1_test_mysql
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
	.getOrCreate()

input_df = spark.read.jdbc(url='jdbc:mysql://up01:3306/edu',
                           table='base_region',
                           properties={'user':'root','password':'123456'})

#3.处理数据
input_df.printSchema()
input_df.show()

#4.保存数据，保存到MySQL中
input_df.write.jdbc(url='jdbc:mysql://up01:3306/edu',
                    table='base_region42',
                    mode='overwrite',
                    properties={'user':'root','password':'123456'})
# 关闭SparkSession
spark.stop()
