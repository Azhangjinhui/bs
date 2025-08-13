import mysql.connector
import csv
from pathlib import Path
mydb = mysql.connector.connect(
	host="node01",  # MySQL 主机地址，根据实际情况修改
	user="root",  # 你的 MySQL 用户名
	password="123456",  # 你的 MySQL 密码
	database="carbon"  # 数据库名称
)

mycursor = mydb.cursor()
csv_folder = Path("../各国19-24年排放量/")
mycursor.execute("TRUNCATE TABLE all_country_carbon_2019_2024")

for csv_file in csv_folder.glob("*.csv"):
	print(csv_file)
	total_rows = 0
	with open(csv_file, 'r', encoding='utf-8') as file:
		reader = csv.reader(file)
		# 跳过表头行
		next(reader)
		for row in reader:
			# 跳过空行（判断行是否为空列表或仅包含空白字符）
			if not row or all(cell.strip() == '' for cell in row):
				continue
			area = row[0]
			co2_mt = float(row[1])
			sector = row[2]
			year = int(row[3])
			sql = "INSERT INTO all_country_carbon_2019_2024 (area,co2_mt,sector,year) VALUES (%s, %s, %s, %s)"
			val = (area, co2_mt, sector, year)
			mycursor.execute(sql, val)
			total_rows +=1
	mydb.commit()
	print(total_rows)
mycursor.close()
mydb.close()