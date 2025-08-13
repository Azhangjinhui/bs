from pyspark.sql import SparkSession
import os

from cn.zhang.tag.base.BaseModel import BaseModel
import pyspark.sql.functions as F
"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	ConsumerCycleModel
   Author      :	itcast team
-------------------------------------------------
"""
# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class ConsumerCycleModel(BaseModel):
	def compute(self,es_df,five_df):
		es_df = es_df.groupBy("memberid").agg(F.max("finishtime").alias("finishtime"))
		es_df=es_df.select('memberid',F.datediff(F.current_date(),F.from_unixtime('finishtime',format='yyyy-MM-dd'))    .alias('days'))
		es_df.show()
		five_df=five_df.select('id',F.split('rule','-')[0].alias('start'),F.split('rule','-')[1].alias('end'))
		five_df.show()
		res_df=es_df.join(five_df,es_df['days'].between(five_df['start'],five_df['end']),how='left').select(es_df['memberid'].alias('userId'),five_df['id'].alias('tagsId'))
		return  res_df
if __name__=='__main__':
	model=ConsumerCycleModel(23)
	model.execute()