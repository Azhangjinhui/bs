
from pyspark.sql import SparkSession
import os

from pyspark.sql.types import StringType

from cn.zhang.tag.bean.ESMeta import ruleToESMeta
import pyspark.sql.functions as F
"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	AgeModel
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
	.appName("SparkSQLAppName") \
	.config("spark.sql.shuffle.partitions", 4) \
	.getOrCreate()
#todo step1：从MySQL中读取四级标签年龄段的数据，并获取rule，提取要读取的ES中的数据内容，转换成ESMeta对象
input_df=spark.read.jdbc(url='jdbc:mysql://up01:3306/tfec_tags',table='tbl_basic_tag',properties={'user':'root','password':'123456'})
four_df=input_df.where('id=14').select('rule')
rule = four_df.first()['rule']
esMeta = ruleToESMeta(rule)
# four_df.show(truncate=False)
# print(esMeta.inType)

#todo step2：根据step1中的信息，读取ES中需要用到的业务数据：用户的id、用户的出生日期birthday，去掉分隔符
es_df=spark.read.format('es').option('es.resource',esMeta.esIndex).option('es.nodes',esMeta.esNodes).option('es.read.field.include',esMeta.selectFields) .option("es.mapping.date.rich","False").load()
es_df=es_df.select('id',F.regexp_replace('birthday','-','').alias('birthday'))
es_df.show()

#todo step3：从MySQL中读取五级标签年龄段所有的值，并拆解成start和end范围
five_df=input_df.where('pid=14').select('id',F.split('rule','-')[0].alias('start'),F.split('rule','-')[1].alias('end'))
five_df.show()

#todo  step4 根据ES中用户的birthday对比五级标签，标记每个用户的年龄段标签
result_df=es_df.join(other=five_df,on= es_df['birthday'].between(five_df['start'],five_df['end']),how='left').select(es_df['id'].cast(StringType()).alias("userId"),five_df['id'].cast(StringType()).alias("tagsId"))
result_df.show()

# todo  step5 将每个用户的年龄段标签数据写入ES中
result_df.write \
	.mode("append") \
	.format("es") \
	.option("es.resource","tags_result") \
	.option("es.nodes",esMeta.esNodes) \
	.option("es.mapping.id","userId") \
	.save()

	







# 关闭SparkSession
spark.stop()
