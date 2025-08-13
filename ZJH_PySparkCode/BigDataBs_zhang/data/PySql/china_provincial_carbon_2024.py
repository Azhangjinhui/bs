import mysql.connector
import csv

# 建立与 MySQL 服务器的连接
mydb = mysql.connector.connect(
	host="node01",  # MySQL 主机地址，根据实际情况修改
	user="root",  # 你的 MySQL 用户名
	password="123456",  # 你的 MySQL 密码
	database="carbon"  # 数据库名称
)

# 创建一个游标对象
mycursor = mydb.cursor()

# 打开 CSV 文件并读取数据
with open('../中国各省24年排放量/各省市24年各行业排放总量.csv', 'r', encoding='utf-8') as file:
	reader = csv.reader(file)
	# 跳过表头行
	next(reader)
	for row in reader:
		province = row[0]
		co2_mt = float(row[1])
		sector = row[2]
		year = int(row[3])

		sql = "INSERT INTO china_provincial_carbon_2024 (province, co2_mt, sector,year) VALUES (%s, %s, %s, %s)"
		val = (province, co2_mt, sector, year)

		mycursor.execute(sql, val)

# 提交事务
mydb.commit()

# 关闭游标和连接
mycursor.close()
mydb.close()