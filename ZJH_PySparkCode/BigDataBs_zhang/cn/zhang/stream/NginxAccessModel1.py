import datetime

import requests
import user_agents
from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

from cn.zhang.stream.base.StreamingBaseModel import StreamingBaseModel

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	NginxAccessModel1
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

#时间处理函数
@F.udf(returnType=StringType())
def parse_access_time(date_str):
	datetime_str = date_str.replace(" +0800", "")
	# 把时间转换为datetime对象
	date_obj = datetime.datetime.strptime(datetime_str, '%d/%b/%Y:%H:%M:%S')
	# 把datetime对象转换为模板时间字符串
	date_result = date_obj.strftime('%Y-%m-%d %H:%M:%S')
	return date_result

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

#ua解析
@F.udf(returnType=StringType())
def parse_user_agent(ua):
	ua_obj = user_agents.parse(ua)
	os = ua_obj.os.family  # NetBSD
	device = ua_obj.device.family  # Other
	browser = ua_obj.browser.family  # Chrome
	result = f'{os},{device},{browser}'
	return result


class NginxAccessModel1(StreamingBaseModel):
	def etl_data(self, input_df):
		#选择Kafka中的value字段，转换为string类型
		input_df = input_df.selectExpr("cast(value as string)")
		#使用正则表达式提取value字段的数据
		pattern_str = '(?<ip>\d+\.\d+\.\d+\.\d+) (- - \[)(?<datetime>[\s\S]+)(?<t1>\][\s"]+)(?<request>[A-Z]+) (?<url>[\S]*) (?<protocol>[\S]+)["] (?<code>\d+) (?<sendbytes>\d+) ["](?<refferer>[\S]*) ["](?<useragent>[\S\s]+)["] ["](?<proxyaddr>[\S\s]+)["]'
		input_df = input_df.select(F.regexp_extract(input_df['value'], pattern_str, 1).alias("ip"),
		                           F.regexp_extract(input_df['value'], pattern_str, 3).alias("datetime"),
		                           F.regexp_extract(input_df['value'], pattern_str, 4).alias("t1"),
		                           F.regexp_extract(input_df['value'], pattern_str, 5).alias("request"),
		                           F.regexp_extract(input_df['value'], pattern_str, 6).alias("url"),
		                           F.regexp_extract(input_df['value'], pattern_str, 7).alias("protocol"),
		                           F.regexp_extract(input_df['value'], pattern_str, 8).alias("code"),
		                           F.regexp_extract(input_df['value'], pattern_str, 9).alias("sendbytes"),
		                           F.regexp_extract(input_df['value'], pattern_str, 10).alias("refferer"),
		                           F.regexp_extract(input_df['value'], pattern_str, 11).alias("useragent"),
		                           F.regexp_extract(input_df['value'], pattern_str, 12).alias("proxyaddr")
		                           )
		#自定义函数，实现时间处理
		input_df = input_df.withColumn("datetime", parse_access_time("datetime"))
		# 自定义函数，实现ip地址解析
		input_df = input_df.withColumn("area", ip_to_address("ip"))
		# 自定义函数，实现UA解析
		input_df = input_df \
			.withColumn("os", F.split(parse_user_agent("useragent"), ',')[0]) \
			.withColumn("device", F.split(parse_user_agent("useragent"), ',')[1]) \
			.withColumn("browser", F.split(parse_user_agent("useragent"), ',')[2])
		return input_df

	def process_data(self, etl_df):
		# 需求统计
		result_df = etl_df.groupby("ip").agg(F.count("ip").alias("pv"),
		                                     F.lit(1).alias("uv"),
		                                     F.first("area").alias("area"),
		                                     F.first("code").alias("code"),
		                                     F.first("os").alias("os"),
		                                     F.first("device").alias("device"),
		                                     F.first("browser").alias("browser"),
		                                     F.first("datetime").alias("datetime")
		                                     )
		return result_df


if __name__ == '__main__':
	#offset偏移量，可以自己指定，语法如下：{"tfec_access_topic":{"0":130}}
	#0：分区号
	#130：offset偏移量的值
	model = NginxAccessModel1(master='local[2]',
	                          numPartitions='4',
	                          broker='up01:9092',
	                          topic='tfec_access_topic',
	                          offset=""" {"tfec_access_topic":{"0":115}} """,
	                          result_table='nginx_access1')
	model.execute()

