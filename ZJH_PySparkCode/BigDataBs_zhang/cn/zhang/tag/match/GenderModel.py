from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

from cn.zhang.tag.bean.ESMeta import ruleToESMeta

"""
-------------------------------------------------
   Description :	TODO：
   SourceFile  :	GenderModel
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

#todo step1：从MySQL中读取四级标签性别的数据，并获取rule，提取要读取的ES中的数据内容转换成ESMeta对象
input_df = spark.read.jdbc(url='jdbc:mysql://up01:3306/tfec_tags',
                           table='tbl_basic_tag',
                           properties={'user':'root','password':'123456'})
four_df = input_df.where('id = 4').select("rule")
#获取rule字符串数据
rule = four_df.first()['rule']
#把rule字符串转换为ESMeta对象
esMeta = ruleToESMeta(rule)
# four_df.printSchema()
# four_df.show(truncate=False)
print(esMeta)

#todo step2：根据step1中的信息，读取ES中需要用到的业务数据：用户的id、用户的性别gender
es_df = spark.read.format("es") \
	.option("es.resource",esMeta.esIndex) \
	.option("es.nodes",esMeta.esNodes) \
	.option("es.read.field.include",esMeta.selectFields) \
	.load()
# es_df.printSchema()
# es_df.show()

#todo step3：从MySQL中读取五级标签性别所有的值
five_df = input_df.where("pid = 4").select("id","rule")
# five_df.printSchema()
# five_df.show()

#todo step4：根据ES中用户的gender对比五级标签，标记每个用户的性别标签
new_df = es_df.join(other=five_df,
                    on=es_df['gender'] == five_df['rule'],
                    how='left').select(es_df['id'].alias("userId"),five_df['id'].alias("tagsId"))
new_df.printSchema()
new_df.show()

#todo step5：读取历史标签结果,old_df
old_df = spark.read \
	.format("es") \
	.option("es.resource","tags_result") \
	.option("es.nodes",esMeta.esNodes) \
	.load()
old_df.printSchema()
old_df.show()

#todo step6：把历史标签结果(old_new)和新的标签(new_df)进行合并
#自定义函数如何注册到Spark程序，方式有三种：
#方式一：spark.udf.register(SQL中的函数名，自定义的python函数名，返回值类型)
#使用场景：既可以在SQL中使用，又可以在DSL中使用
#方式二：F.udf(自定义的Python函数名，返回值类型)
#使用场景：只能在DSL中使用，无法在SQL中使用。
#方式三：@F.udf(返回值类型)
#使用场景：只能在DSL中使用。无法在SQL中使用。
#总结：以上三种方式，只有方式一既可以在SQL中使用，又可以在DSL中使用。方式二和方式三，只能在DSL中使用。
@F.udf(returnType=StringType())
def merge_tags(new_tags, old_tags):
	#1.如果old_tags为空，则返回new_tags
	if old_tags is None:
		return new_tags
	#2.如果new_tags为空，则返回old_tags
	elif new_tags is None:
		return old_tags
	#3.如果都不为空，则进行合并
	else:
		#对new_tags进行切分
		new_tags_list = str(new_tags).split(",")
		#对old_tags进行切分
		old_tags_list = str(old_tags).split(",")
		#对切分后的结果进行合并
		result_tags = new_tags_list + old_tags_list
		#把列表拼接成字符串返回
		return ','.join(set(result_tags))


result_df = new_df.join(other=old_df,
                        on=new_df['userId'] == old_df['userId'],
                        how='left') \
	.select(new_df['userId'].cast(StringType()),
            merge_tags(new_df['tagsId'],old_df['tagsId']).alias("tagsId"))
result_df.printSchema()
result_df.show()

#todo step7：把合并后的标签结果写入到ES中
result_df.write \
	.mode("append") \
	.format("es") \
	.option("es.resource","tags_result") \
	.option("es.nodes",esMeta.esNodes) \
	.option("es.mapping.id","userId") \
	.save()


# 关闭SparkSession
spark.stop()
