from pyspark.sql import SparkSession
import os
import  pyspark.sql.functions as F
from cn.zhang.stream.base.StreamingBaseModel import StreamingBaseModel

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	UserEventModel1
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class UserEventModel1(StreamingBaseModel):

    def etl_data(self, input_df):
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

        return input_df
    def process_data(self, etl_df):
        input_df=etl_df.groupby('user_id').agg(F.count('is_browse').alias('browse_cnt'),F.sum('is_order').alias('order_cnt'),F.sum('is_buy').alias('buy_cnt'),
                                         F.sum('is_back_order').alias('back_order_cnt'),F.sum('is_received').alias('received_cnt'),
                                         )
        return input_df
if __name__ == '__main__':
    model = UserEventModel1(master='local[2]',
                            numPartitions='4',
                            broker='up01:9092',
                            topic='user_event',
                            offset='earliest',
                            result_table='user_event1')
    model.execute()
