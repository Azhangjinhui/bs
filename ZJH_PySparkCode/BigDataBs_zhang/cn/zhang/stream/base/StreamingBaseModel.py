from pyspark.sql import SparkSession
import os

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	StreamingBaseModel
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class StreamingBaseModel(object):
	"""
	流式基类，后面的流式任务需要继承基类
	0.初始化环境
	1.读取Kafka的数据
	2.对数据做ETL操作
	3.指标统计分析
	4.保存结果
	"""

	#初始化环境
	def __init__(self,master,numPartitions,broker,topic,offset,result_table):
		self.master = master
		self.numPartitions = numPartitions
		self.broker = broker
		self.topic = topic
		self.offset = offset
		self.result_table = result_table
		self.spark = SparkSession \
			.builder \
			.master(f"{self.master}") \
			.appName("SparkSQLAppName") \
			.config("spark.sql.shuffle.partitions", f'{self.numPartitions}') \
			.getOrCreate()


	#读取Kafka的数据
	def read_data_from_kafka(self):
		input_df = self.spark.readStream \
			.format("kafka") \
			.option("kafka.bootstrap.servers", f"{self.broker}") \
			.option("subscribe", f"{self.topic}") \
			.option("startingOffsets", f"{self.offset}") \
			.load()
		return input_df

	#对数据做ETL操作，实现的时候一定要返回etl后的数据
	def etl_data(self,input_df):
		pass

	#指标统计分析，拿着ETL后的数据来进行分组聚合，统计结果后的数据为result_df，要记得返回
	def process_data(self,etl_df):
		pass

	#保存结果
	def save_result_to_mysql(self,result_df):
		query1 = result_df.writeStream.format("console").outputMode("complete")

		def save_to_mysql(df, epoch_id):
			# df就是批量写出的df，可以使用SparkSQL的写出语法
			df.write.jdbc(url='jdbc:mysql://up01:3306/tfec_stream_result',
			              table=f'{self.result_table}',
			              mode='overwrite',
			              properties={"user": "root", "password": "123456"})

		query2 = result_df.writeStream.outputMode("complete").foreachBatch(save_to_mysql)

		#启动流式任务
		query1.start()
		query2.start().awaitTermination()


	#额外创建一个方法，把上述定义的流程串起来执行
	def execute(self):
		#init不需要调用，对象创建时会自动运行
		#读取Kafka的数据
		input_df = self.read_data_from_kafka()
		#调用ETL处理方法，返回处理后的数据
		etl_df = self.etl_data(input_df)
		#对处理后的数据进行指标聚合统计分析
		result_df = self.process_data(etl_df)
		#把结果保存到MySQL
		self.save_result_to_mysql(result_df)



