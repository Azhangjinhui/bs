from pyspark.sql import SparkSession, DataFrame
import os
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

from cn.zhang.tag.bean.ESMeta import ruleToESMeta

"""
-------------------------------------------------
   Description :	TODO：基类重构
   SourceFile  :	BaseModel
   Author      :	itcast team
-------------------------------------------------
"""

# 0.设置系统环境变量
os.environ['JAVA_HOME'] = '/export/server/jdk1.8.0_241/'
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/envs/pyspark_env/bin/python'


@F.udf(returnType=StringType())
def merge_tags(new_tags, old_tags,five_id_str):
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

		"""
		标签更新：
		（2）在标签合并时，进行循环判断，如果历史标签结果中有id在新传入的five_id_str中，则删除，否则不管（保留）    
		"""
		#five_id_list：[24,25,26,27,28,29]
		five_id_list = five_id_str.split(",")
		for tag in five_id_list:
			#当tag为29时，它在old_tag_list中，因此判断成立，执行删除逻辑
			if tag in old_tags_list:
				old_tags_list.remove(tag)

		#对切分后的结果进行合并
		result_tags = new_tags_list + old_tags_list
		#把列表拼接成字符串返回
		return ','.join(set(result_tags))



class BaseModel(object):
	"""
	用户自定义的基类，在这个类中定义标签的步骤
	第一部分：
		#0.初始化Spark环境
		#1.读取MySQL标签体系数据
		#2.过滤4级标签的数据，将四级标签的rule转换为esMeta对象
		#3.根据esMeta对象从ES中读取相应的业务数据
		#4.根据4级标签ID，读取5级标签的数据
		#5.通过ES中的业务数据与MySQL的5级标签进行打标签
		#6.从ES中读取历史用户标签数据
		#7.将老的用户画像标签与新的标签进行合并，得到最终标签
		#8.将最终的结果写入ES中
		#9.销毁Spark环境，释放资源
	"""

	# 0.初始化Spark环境
	def __init__(self,fourId):
		#把spark变量声明为类的属性，以方便在下面的步骤继续使用
		self.spark = SparkSession \
			.builder \
			.master("local[2]") \
			.appName("SparkSQLAppName") \
			.config("spark.sql.shuffle.partitions", 4) \
			.getOrCreate()
		self.fourId = fourId

	# 1.读取MySQL标签体系数据
	def read_from_mysql(self):
		input_df = self.spark.read.jdbc(url='jdbc:mysql://up01:3306/tfec_tags',
		                                table='tbl_basic_tag',
		                                properties={'user': 'root', 'password': '123456'})
		return input_df

	# 2.过滤4级标签的数据，将四级标签的rule转换为esMeta对象
	def rule_to_es_meta(self,input_df):
		four_df = input_df.where(f'id = {self.fourId}').select("rule")
		# 获取rule字符串数据
		rule = four_df.first()['rule']
		# 把rule字符串转换为ESMeta对象
		esMeta = ruleToESMeta(rule)
		return esMeta

	# 3.根据esMeta对象从ES中读取相应的业务数据
	def read_from_es(self,esMeta):
		es_df = self.spark.read.format("es") \
			.option("es.resource", esMeta.esIndex) \
			.option("es.nodes", esMeta.esNodes) \
			.option("es.read.field.include", esMeta.selectFields) \
			.option("es.mapping.date.rich", "False") \
			.load()
		return es_df

	# 4.根据4级标签ID，读取5级标签的数据
	def get_five_tags(self,input_df):
		five_df: DataFrame = input_df.where(f"pid = {self.fourId}").select("id", "rule")
		return five_df

	# 5.通过ES中的业务数据与MySQL的5级标签进行打标签
	#打标签需要业务数据（es_df）和标签规则数据（five_df）
	#当这个方法在子类实现后，也就是标签打完了，要记得返回新的标签结果（new_df）
	def compute(self,es_df,five_df):
		pass

	# 6.从ES中读取历史用户标签数据
	def read_old_df_from_es(self,esMeta):
		old_df = self.spark.read \
			.format("es") \
			.option("es.resource", "tags_result") \
			.option("es.nodes", esMeta.esNodes) \
			.load()
		return old_df

	# 7.将老的用户画像标签与新的标签进行合并，得到最终标签
	def merge_new_df_and_old_df(self,new_df,old_df,five_id_str):
		result_df = new_df.join(other=old_df,
		                        on=new_df['userId'] == old_df['userId'],
		                        how='left') \
			.select(new_df['userId'].cast(StringType()),
		            merge_tags(new_df['tagsId'], old_df['tagsId'],five_id_str).alias("tagsId"))
		return result_df

	# 8.将最终的结果写入ES中
	def save_result_df_to_es(self,result_df,esMeta):
		result_df.write \
			.mode("append") \
			.format("es") \
			.option("es.resource", "tags_result") \
			.option("es.nodes", esMeta.esNodes) \
			.option("es.mapping.id", "userId") \
			.save()

	# 9.销毁Spark环境，释放资源
	def close(self):
		self.spark.stop()


	#第二部分
	#额外定义一个函数（方法），把上述10个函数串联起来执行
	def execute(self):
		#1.读取MySQL标签体系数据
		input_df = self.read_from_mysql()
		#2.过滤4级标签的数据，将四级标签的rule转换为esMeta对象
		esMeta = self.rule_to_es_meta(input_df)
		#3.根据esMeta对象从ES中读取相应的业务数据
		es_df = self.read_from_es(esMeta)
		#4.根据4级标签ID，读取5级标签的数据
		five_df = self.get_five_tags(input_df)

		"""
		标签更新：
		（1）由five_df得到该4级标签下所有5级标签的id值(list列表）
		（2）把这个结果传入给标签合并时使用，在合并时进行遍历判断
		"""
		#five_id_list：[24,25,26,27,28,29]
		five_id_list = five_df.select("id").rdd.map(lambda row:row['id']).collect()
		#five_id_str：'24,25,26,27,28,29'
		five_id_str = ",".join(str(i) for i in five_id_list)

		#5.通过ES中的业务数据与MySQL的5级标签进行打标签
		#当这个方法在子类实现后，也就是标签打完了，要记得返回新的标签结果（new_df）
		new_df = self.compute(es_df,five_df)
		try:
			#6.从ES中读取历史用户标签数据
			old_df = self.read_old_df_from_es(esMeta=esMeta)
			#7.将老的用户画像标签与新的标签进行合并，得到最终标签
			#把five_id_str使用lit函数包裹（常量列必须使用lit函数包起来）
			result_df = self.merge_new_df_and_old_df(new_df,old_df,F.lit(five_id_str))
		except:
			#如上代码进入这部分运行，说明old_df为空，也就是第一次执行标签代码
			print("--------------首次运行，跳过合并----------------")
			result_df = new_df
		#8.将最终的结果写入ES中
		self.save_result_df_to_es(result_df,esMeta)
		#9.销毁Spark环境，释放资源
		self.close()


