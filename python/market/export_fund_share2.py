#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 从数据库里面导出一定时间前的还持有份额的人员和产品数据，每个产品是一个Excel

import pymysql
from openpyxl import *
import os

#检索每一行的第一个产品代码字段，如果是同一个代码，要保存在一个Excel里，不同产品的数据，用不同的Excel保存
#fields是列名，data是数据集，path是保存的路径，如果空，则保存在当前目录下
def SaveData2Excel(fields, data, path = ''):
	if path == '':
		path = os.getcwd()
	wb = Workbook()
	ws = wb.active
	fundcode = data[0][0]
	fundname = data[0][1]
	#第1行是列名
	ws.append([f[0] for f in fields])
	#把数据复制到Excel中
	for row in data:
		#不是同一个产品，先保存原来的Excel，再新建一个
		if row[0] != fundcode:
			wb.save(path + os.sep + fundname + "_持有人名册.xlsx")
			print("{0}结束导出".format(fundname))
			wb = Workbook()
			ws = wb.active
			fundcode = row[0]
			fundname = row[1]
			ws.append([f[0] for f in fields])
		ws.append(row)
	wb.save(path + os.sep + fundname + "_持有人名册.xlsx")
	wb = None

#需要导出数据的日期范围
end_date = "2018-1-1"
#导出文件地址
path = "C:\\Users\\gaos\\Documents\\PyqtProject\\output"
#数据库地址
connection = pymysql.connect(host='192.168.40.98', port=3306,\
	user='selling_query',password='123456',db='private_data',charset='utf8')
cursor = connection.cursor()
#导出的SQL
sql_base = "SELECT \
	p.`code` as '产品代码', \
	p.`name` AS '产品名', \
	u.`name` AS '用户名', \
	concat(" + '"' + "'"+ '"' + ",u.certificate_no) as '认证号码',  \
  h.current_share as '2017年末份额' \
FROM \
	holders h, \
	users u, \
	products p, \
	( \
		SELECT \
		h1.product_id, \
		h1.user_id, \
		max(h1.data_log_id) log_id \
	FROM \
		holders h1, \
		users u, \
		products p \
	WHERE \
		TO_DAYS(h1.hold_at_str) <= TO_DAYS('{0}') \
	AND h1.product_id = p.id \
	AND h1.user_id = u.id \
	GROUP BY \
		h1.product_id, \
		h1.user_id \
	) t \
WHERE \
	1 = 1 \
AND t.log_id = h.data_log_id \
AND t.product_id = h.product_id  \
and t.user_id = h.user_id \
and h.current_share > 0 \
AND h.product_id = p.id \
AND p.`status` = 0 \
AND p.company_id = 1 \
and h.user_id = u.id \
ORDER BY \
	h.product_id, \
	h.user_id;"

#从数据库获取数据
sql = sql_base.format(end_date)
cursor.execute(sql)
result = cursor.fetchall()
if len(result) > 0:
	fields = cursor.description
	SaveData2Excel(fields, result, path)

#关闭数据库
cursor.close()
connection.close()