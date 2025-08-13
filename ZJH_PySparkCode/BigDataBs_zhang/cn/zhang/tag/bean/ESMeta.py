
class ESMeta(object):
	"""
	自定义的EsMeta类，用来封装标签规则的属性信息，以方便后续使用
	"""
	inType:str = None
	esNodes:str = None
	esIndex:str = None
	esType:str = None
	selectFields:str = None

	#每一个对象创建，默认都会走init方法（初始化）
	def __init__(self,inType,esNodes,esIndex,esType,selectFields):
		self.inType = inType
		self.esNodes = esNodes
		self.esIndex = esIndex
		self.esType = esType
		self.selectFields = selectFields

	def __str__(self):
		"""
		重写str魔术方法，对象初始化后，结果我们肉眼就能读懂了。
		:return: 重写后的字符串
		"""
		return f'{self.inType},{self.esType},{self.esNodes},{self.esIndex},{self.selectFields}'

def ruleToESMeta(rule):
	"""
	标签规则数据转换为ESMeta对象的方法
	:param rule: 标签规则数据，这是一个字符串
	:return: ESMeta对象
	"""
	#列表中一共有5个值，格式是：key=value，比如inType=Elasticsearch
	lists = rule.split("##")
	ruleDict = {}
	for ruleKV in lists:
		#kvStr[0] = key
		#kvStr[1] = value
		kvStr = ruleKV.split("=")
		ruleDict[kvStr[0]] = kvStr[1]
	# **：专门解析转换dict类型的数据
	return ESMeta(**ruleDict)



if __name__ == '__main__':
	rule = "inType=Elasticsearch##esNodes=up01:9200##esIndex=tfec_tbl_users##esType=_doc##selectFields=id,gender"
	#根据输入的rule规则，解析返回一个EsMeta对象
	esMeta = ruleToESMeta(rule)
	print(esMeta) # <__main__.ESMeta object at 0x7fc7b525cd10> 内存地址值
	print(esMeta.inType)
	print(esMeta.esNodes)
	print(esMeta.esIndex)
	print(esMeta.esType)
	print(esMeta.selectFields)