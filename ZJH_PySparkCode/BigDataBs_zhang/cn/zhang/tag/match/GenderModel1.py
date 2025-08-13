from pyspark.sql import SparkSession
import os

from cn.zhang.tag.base.BaseModel import BaseModel
from cn.zhang.tag.match.GenderModel import result_df, old_df

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	GenderModel1
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class GenderModel1(BaseModel):
	def compute(self,es_df,five_df):
		es_df.show(10)
		five_df.show(10)
		new_df = es_df.join(other=five_df,
		                    on=es_df['gender'] == five_df['rule'],
		                    how='left').select(es_df['id'].alias("userId"), five_df['id'].alias("tagsId"))
		return new_df
if __name__=='__main__':
	gender_model = GenderModel1(4)
	gender_model.execute()