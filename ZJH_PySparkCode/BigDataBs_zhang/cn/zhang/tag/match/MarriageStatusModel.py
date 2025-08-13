from pyspark.sql import SparkSession
import os

from cn.zhang.tag.base.BaseModel import BaseModel

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	MarriageStatusModel
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class MarriageStatusModel(BaseModel):
	def compute(self,es_df,five_df):
		es_df.show()
		five_df.show()
		res_df=es_df.join(five_df,es_df['marriage']==five_df['rule'],'left').select(es_df['id'].alias('userId'),five_df['id'].alias('tagsId'))
		return  res_df
if __name__=='__main__':
	model=MarriageStatusModel(66)
	model.execute()