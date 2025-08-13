from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

from cn.zhang.tag.base.BaseModel import BaseModel

"""
-------------------------------------------------
   Description :	TODO：年龄段标签重构代码
   SourceFile  :	AgeModel1
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'

class AgeModel1(BaseModel):
	def compute(self, es_df, five_df):
		"""
		#打标签的代码，得自己实现
		:param es_df: 业务数据
		:param five_df: 标签规则数据
		:return: 标签结果
		"""
		#业务数据处理
		es_df = es_df.select("id", F.regexp_replace("birthday", "-", "").alias("birthday"))
		es_df.printSchema()
		es_df.show()
		#标签规则数据处理
		five_df = five_df.select("id",
		                         F.split("rule", "-")[0].alias("start"),
		                         F.split("rule", "-")[1].alias("end"))
		five_df.printSchema()
		five_df.show()
		#打标签实现
		new_df = es_df.join(other=five_df,
		                    on=es_df['birthday'].between(five_df['start'], five_df['end']),
		                    how='left').select(es_df['id'].cast(StringType()).alias("userId"),
		                                       five_df['id'].cast(StringType()).alias("tagsId"))
		return new_df


if __name__ == '__main__':
	ageModel = AgeModel1(14)
	ageModel.execute()