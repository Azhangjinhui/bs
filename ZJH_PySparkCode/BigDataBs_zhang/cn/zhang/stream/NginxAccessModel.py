import datetime

import requests
import user_agents
from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

"""
-------------------------------------------------
   Description :	TODO：NginxAccess访问日志流式处理
   SourceFile  :	NginxAccessModel
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

#2.读取Kafka的数据
input_df = spark.readStream \
	.format("kafka") \
	.option("kafka.bootstrap.servers","up01:9092") \
	.option("subscribe","tfec_access_topic") \
	.option("startingOffsets","earliest") \
	.load()

#3.处理数据
input_df.printSchema()
input_df = input_df.selectExpr("cast(value as string)")

#使用正则函数对数据进行解析（提取）
#regexp_extract(str,pattern,idx)，正则提取函数，需要使用Java版的正则
#str：数据
#pattern：正则表达式
#idx：索引
pattern_str = '(?<ip>\d+\.\d+\.\d+\.\d+) (- - \[)(?<datetime>[\s\S]+)(?<t1>\][\s"]+)(?<request>[A-Z]+) (?<url>[\S]*) (?<protocol>[\S]+)["] (?<code>\d+) (?<sendbytes>\d+) ["](?<refferer>[\S]*) ["](?<useragent>[\S\s]+)["] ["](?<proxyaddr>[\S\s]+)["]'
input_df = input_df.select(F.regexp_extract(input_df['value'],pattern_str,1).alias("ip"),
                           F.regexp_extract(input_df['value'],pattern_str,3).alias("datetime"),
                           F.regexp_extract(input_df['value'],pattern_str,4).alias("t1"),
                           F.regexp_extract(input_df['value'],pattern_str,5).alias("request"),
                           F.regexp_extract(input_df['value'],pattern_str,6).alias("url"),
                           F.regexp_extract(input_df['value'],pattern_str,7).alias("protocol"),
                           F.regexp_extract(input_df['value'],pattern_str,8).alias("code"),
                           F.regexp_extract(input_df['value'],pattern_str,9).alias("sendbytes"),
                           F.regexp_extract(input_df['value'],pattern_str,10).alias("refferer"),
                           F.regexp_extract(input_df['value'],pattern_str,11).alias("useragent"),
                           F.regexp_extract(input_df['value'],pattern_str,12).alias("proxyaddr")
                           )

#时间处理函数
@F.udf(returnType=StringType())
def parse_access_time(date_str):
	datetime_str = date_str.replace(" +0800", "")
	# 把时间转换为datetime对象
	date_obj = datetime.datetime.strptime(datetime_str, '%d/%b/%Y:%H:%M:%S')
	# 把datetime对象转换为模板时间字符串
	date_result = date_obj.strftime('%Y-%m-%d %H:%M:%S')
	return date_result

#withColumn(列名，列的处理逻辑)，如果列存在则会替换，如果列不存在，则新增
input_df = input_df.withColumn("datetime",parse_access_time("datetime"))


#ip地址解析
@F.udf(returnType=StringType())
def ip_to_address(ip):
	url = f'http://opendata.baidu.com/api.php?query={ip}&co=&resource_id=6006&oe=utf8'
	# 发送GET请求url，服务器会相应数据，接受响应数据即可
	# get，REST API，表示查询
	try:
		res = requests.get(url).json()
		address = res['data'][0]['location']
		return address
	except:
		print("------------解析失败------------")
		return '未知地址'
#自定义函数，实现ip地址解析
input_df = input_df.withColumn("area",ip_to_address("ip"))

@F.udf(returnType=StringType())
def parse_user_agent(ua):
	ua_obj = user_agents.parse(ua)
	os = ua_obj.os.family  # NetBSD
	device = ua_obj.device.family  # Other
	browser = ua_obj.browser.family  # Chrome
	result = f'{os},{device},{browser}'
	return result

#自定义函数，实现UA解析
input_df = input_df \
	.withColumn("os",F.split(parse_user_agent("useragent"),',')[0]) \
	.withColumn("device",F.split(parse_user_agent("useragent"),',')[1]) \
	.withColumn("browser",F.split(parse_user_agent("useragent"),',')[2])


#需求统计
result_df = input_df.groupby("ip").agg(F.count("ip").alias("pv"),
                                       F.lit(1).alias("uv"),
                                       F.first("area").alias("area"),
                                       F.first("code").alias("code"),
                                       F.first("os").alias("os"),
                                       F.first("device").alias("device"),
                                       F.first("browser").alias("browser"),
                                       F.first("datetime").alias("datetime")
                                       )

#4.写出数据
query1 = result_df.writeStream.format("console").outputMode("complete")
#foreachBatch自定义函数，用于数据写出
def foreach_batch_function(df, epoch_id):
	#数据处理，把DF按照离线批量的方式写出
	df.write.jdbc(url='jdbc:mysql://up01:3306/tfec_stream_result',
	              table='nginx_access',
	              mode='overwrite',
	              properties={'user':'root','password':'123456'})

query2 = result_df.writeStream.outputMode("complete").foreachBatch(foreach_batch_function)
# 启动流任务
query1.start()
query2.start().awaitTermination()
