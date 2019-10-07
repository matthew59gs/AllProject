# -*- coding:utf-8 -*-

import pymysql
import datetime
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

logger = dunhe_public.SetLog('UserAvgAsset')
try:
	mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
								 user='trader', password='123456',
								 db='tradesplit',
								 charset='utf8')
except Exception as e:
	logger.error("mysql connect fail: {0}".format(e))
	raise e
else:
	cursor = mysql_conn.cursor()
	try:
		sql = 'SELECT DISTINCT product_id, user_id FROM CusHolding2017 WHERE 1=1 GROUP BY product_id, user_id ORDER BY product_id, user_id;'
		logger.debug('SELECT sql: ' + sql)
		cursor.execute(sql)
		product_user_pair = cursor.fetchall()
		listholdingdata = []

		try:
			for product_id, user_id in product_user_pair:
				sql = 'SELECT date, product_id, user_id, current_share FROM CusHolding2017 WHERE 1=1 AND product_id = {0} and user_id = {1} ORDER BY date, product_id, user_id;'.format(product_id, user_id)
				logger.debug('SELECT sql: ' + sql)
				cursor.execute(sql)
				holdingdata = cursor.fetchall()
				sql = 'SELECT date, product_id, net FROM NetValue2017 WHERE 1=1 AND product_id = {0} ORDER BY date, product_id;'.format(product_id)
				logger.debug('SELECT sql: ' + sql)
				cursor.execute(sql)
				netdata = cursor.fetchall()

				iStart = 0
				last_holding_share = holdingdata[0][0]
				for net_date, net_product, net_value in netdata:
					for i in range(iStart, len(holdingdata)):
						holding_date = holdingdata[i][0]
						holding_product = holdingdata[i][1]
						holding_user = holdingdata[i][2]
						holding_share = holdingdata[i][3]
						if (net_product == holding_product):
							logger.debug('i[{0}] iStart[{1}]'.format(i, iStart))
							logger.debug('net_date[{0}], net_product[{1}], net_value[{2}], holding_date[{3}], holding_product[{4}], holding_user[{5}], holding_share[{6}]'.format( \
								net_date, net_product, net_value, holding_date, holding_product, holding_user, holding_share))
							if (holding_date == net_date):
								listholdingdata.append([net_date, net_product, holding_user, holding_share, net_value])
								last_holding_share = holding_share
								iStart = iStart + 1
								logger.debug('iStart = ' + str(iStart))
							elif (holding_date > net_date):
								listholdingdata.append([net_date, net_product, holding_user, last_holding_share, net_value])
							break
		except Exception as e:
			raise e
	except Exception as e:
		logger.error("Sql execute error: {0}".format(e))
		raise e
	finally:
		cursor.close()
		mysql_conn.close()

	logger.debug('listholdingdata: {0}'.format(listholdingdata))
	if (len(listholdingdata) > 0):
		dunhe_public.WriteData2Excel(listholdingdata, 'G:\\data\\holdingdata.xlsx')
'''
	for net_date, net_product, net_value in netdata:
		new_data = False
		for holding_date, holding_product, holding_user, holding_share in holdingdata:
			if (net_product == holding_product):
				if (holding_date > net_date):
					if new_data:
						listholdingdata.append([net_date, net_product, last_holding_user, last_holding_share, net_value])
						new_data = False
				else:
					new_data = True
					last_holding_user = holding_user
					last_holding_share = holding_share
		if new_data:
			listholdingdata.append([net_date, net_product, last_holding_user, last_holding_share, net_value])
'''

