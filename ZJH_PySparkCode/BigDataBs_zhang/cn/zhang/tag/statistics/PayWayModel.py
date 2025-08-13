from pyspark.sql import SparkSession, Window
import os
import pyspark.sql.functions as F
from cn.zhang.tag.base.BaseModel import BaseModel

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	PayWayModel
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class PayWayModel(BaseModel):
	def compute(self, es_df, five_df):
		#todo:1-先统计每个用户每种支付方式的订单个数
		es_df = es_df.groupby("memberid","paymentcode").agg(F.count("paymentcode").alias("paymentcode_cnt"))
		#todo:2-取用户使用最多的支付方式
		#row_nuber() over(partition by aaa order by bbb) rn
		#开窗函数有三类：
		#类别一：排序类（row_number，rank，dense_rank）
		#类别二：聚合类（max，min，age，count，sum）
		#类别三：分析类（lag，lead）
		#DSL的开窗写法：
		#window.partitionBy().orderBy()
		es_df = es_df.select("memberid",
		                     "paymentcode",
		                     "paymentcode_cnt",
		                     F.row_number().over(Window.partitionBy("memberid").orderBy(F.desc("paymentcode_cnt"))).alias("rn"))
		es_df = es_df.where("rn = 1").select("memberid","paymentcode")
		es_df.show()
		#todo:3-关联支付方式标签
		new_df = es_df.join(five_df,es_df['paymentcode'] == five_df['rule'],'left') \
			.select(es_df['memberid'].alias("userId"),five_df['id'].alias("tagsId"))
		five_df.show()
		new_df.show()
		return new_df


if __name__ == '__main__':
	model = PayWayModel(30)
	model.execute()