from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
"""
-------------------------------------------------
   Description :	TODO：用户行为数据分析
   SourceFile  :	UserEventModel
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

#数据读取
input_df = spark.readStream \
	.format("kafka") \
	.option("kafka.bootstrap.servers","up01:9092") \
	.option("subscribe","user_event") \
	.option("startingOffsets","earliest") \
	.load()

#数据处理
input_df.printSchema()
input_df = input_df.selectExpr("cast(value as string)")

input_df = input_df.select(F.json_tuple("value","phone_num","system_id","user_name","user_id","visit_time","goods_type","minimum_price")
                           .alias("phone_num","system_id","user_name","user_id","visit_time","goods_type","minimum_price"),
                           F.get_json_object("value","$.area.province").alias("province"),
                           F.get_json_object("value","$.area.city").alias("city"),
                           F.get_json_object("value","$.area.sp").alias("sp"),
                           F.get_json_object("value","$.user_behavior.is_browse").alias("is_browse"),
                           F.get_json_object("value","$.user_behavior.is_order").alias("is_order"),
                           F.get_json_object("value","$.user_behavior.is_buy").alias("is_buy"),
                           F.get_json_object("value","$.user_behavior.is_back_order").alias("is_back_order"),
                           F.get_json_object("value","$.user_behavior.is_received").alias("is_received"),
                           F.get_json_object("value","$.goods_detail.goods_name").alias("goods_name"),
                           F.get_json_object("value","$.goods_detail.browse_page").alias("browse_page"),
                           F.get_json_object("value","$.goods_detail.browse_time").alias("browse_time"),
                           F.get_json_object("value","$.goods_detail.to_page").alias("to_page"),
                           F.get_json_object("value","$.goods_detail.to_time").alias("to_time"),
                           F.get_json_object("value","$.goods_detail.page_keywords").alias("page_keywords")
                           )



input_df=input_df.groupby('user_id').agg(F.count('is_browse').alias('browse_cnt'),F.sum('is_order').alias('order_cnt'),F.sum('is_buy').alias('buy_cnt'),
                                F.sum('is_back_order').alias('back_order_cnt'),F.sum('is_received').alias('received_cnt'),
                                )
#数据写出
def save_to_mysql(input_df,epoch_id):
	input_df.write.jdbc(url='jdbc:mysql://up01:3306/tfec_stream_result',table='user_event',mode='overwrite',properties={'user':'root','password':'123456'})


query1 = input_df.writeStream.format("console").outputMode("complete")
query2=input_df.writeStream.outputMode('complete').foreachBatch(save_to_mysql)
# 启动流式任务
query1.start()
query2.start().awaitTermination()

