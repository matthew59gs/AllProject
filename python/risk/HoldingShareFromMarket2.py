#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 从Oplus读取取当日市场数据，形成临时表，进入market_holding表
# 从Oplus读取当日持仓数据，形成临时表，进入company_holding表
# tradesplit库做表汇总分析，形成Excel

import pymysql
import datetime
import os
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

# Oplus库读取市场数据，写入tradesplit库的market_holding表
def GetMarketData():
	market_insert_sql = ''
	try:
		mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
									 user='oplus', password='oplus',
									 db='oplus_p',
									 charset='utf8')
	except Exception as e:
		logger.error("mysql connect fail: {0}".format(e))
		raise e
	else:
		cursor = mysql_conn.cursor()
		try:
			sql = 'SELECT \
				UPPER( t.report_code ) report_code, \
				UPPER( tfk.future_kind_code ) future_kind_code, \
				t.market_no, \
				t.business_date, \
				t.position_quantity / 2 position_quantity \
			FROM \
				tstockinfo_future t, tfuturekind tfk \
			WHERE \
				t.future_kind_id = tfk.future_kind_id \
				AND t.business_date = \'{0}\'  \
				AND t.position_quantity > 0  \
				AND t.market_no IN ( \'3\', \'4\', \'9\', \'34\' ) UNION ALL \
			SELECT \
				UPPER( t.report_code ) report_code, \
				UPPER( tfk.future_kind_code ) future_kind_code, \
				t.market_no, \
				t.business_date, \
				t.position_quantity  \
			FROM \
				tstockinfo_future t, tfuturekind tfk \
			WHERE \
				t.future_kind_id = tfk.future_kind_id \
				and t.business_date = \'{0}\'  \
				AND t.position_quantity > 0  \
				AND t.market_no IN ( \'7\' )'.format(HQ_DATE_OPLUS)
			logger.debug('select sql: ' + sql)
			cursor.execute(sql)
			data = cursor.fetchall()
			logger.info('Get {0} data from market'.format(len(data)))
			for report_code, future_kind_code, market_no, business_date, position_quantity in data:
				market_insert_sql += '(\'{0}\', \'{1}\', \'{2}\', \'{3}\', {4}),'.format(report_code, future_kind_code, market_no, business_date, position_quantity)
			if (len(data) > 0):
				market_insert_sql = 'INSERT INTO market_holding2(report_code, future_kind_code, market_no, business_date, position_quantity) VALUES ' + market_insert_sql
				market_insert_sql = market_insert_sql[:len(market_insert_sql) - 1] + ';'
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))
			raise e
		finally:
			cursor.close()
			mysql_conn.close()
	return market_insert_sql

# Oplus库读取持仓数据，写入tradesplit库的
def GetHoldingData():
	holding_insert_sql = ''
	try:
		mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
									 user='oplus', password='oplus',
									 db='oplus_p',
									 charset='utf8')
	except Exception as e:
		logger.error("mysql connect fail: {0}".format(e))
		raise e
	else:
		cursor = mysql_conn.cursor()
		try:
			sql = 'SELECT \
				business_date, \
				future_kind_code, \
				report_code, \
				position_type, \
				sum( current_amount ) current_amount  \
			FROM \
				( \
			SELECT DISTINCT \
				t.business_date, \
				UPPER( tfk.future_kind_code ) future_kind_code, \
				UPPER( t.report_code ) report_code, \
				t.position_type, \
				t.current_amount, \
				t.fund_id  \
			FROM \
				tfundstock t, \
				tfuturekind tfk, \
				tstockinfo_future tsf  \
			WHERE \
				t.report_code = tsf.report_code  \
				AND tsf.future_kind_id = tfk.future_kind_id  \
				AND t.business_date = \'{0}\'  \
				AND t.market_no IN ( \'3\', \'4\', \'7\', \'9\', \'34\' )  \
				AND t.position_type IN ( \'1\', \'2\' )  \
				AND t.current_amount > 0  \
				) m  \
			GROUP BY \
				business_date, \
				position_type, \
				report_code;'.format(HQ_DATE_OPLUS)
			logger.debug('select sql: ' + sql)
			cursor.execute(sql)
			data = cursor.fetchall()
			logger.info('Get {0} data from oplus'.format(len(data)))
			for business_date, future_kind_code, report_code, position_type, current_amount in data:
				holding_insert_sql += '(\'{0}\', \'{1}\', \'{2}\', \'{3}\', {4}),'.format(business_date, future_kind_code, report_code, position_type, current_amount)
			if (len(data) > 0):
				holding_insert_sql = 'INSERT INTO company_holding2(business_date, future_kind_code, report_code, position_type, current_amount) VALUES ' + holding_insert_sql
				holding_insert_sql = holding_insert_sql[:len(holding_insert_sql) - 1] + ';'
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))
			raise e
		finally:
			cursor.close()
			mysql_conn.close()
	return holding_insert_sql

# Oplus库读取明细持仓数据
## 输入格式：business_date, position_type, report_code
## 返回格式：business_date, report_code, position_type, current_amount, fund_code, fund_name, broker_name, capital_account_no
def GetHoldingDetail(I_data):
	try:
		mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
									 user='oplus', password='oplus',
									 db='oplus_p',
									 charset='utf8')
	except Exception as e:
		logger.error("mysql connect fail: {0}".format(e))
		raise e
	else:
		cursor = mysql_conn.cursor()
		try:
			title = []
			is_title_filled = False
			detail_data = []
			for business_date, position_type, report_code in I_data:
				sql = 'SELECT DISTINCT \
					t.business_date \'日期\', \
					UPPER( t.report_code ) \'合约代码\', \
					CASE  \
						WHEN t.position_type =\'1\' THEN \'多\'  \
						WHEN t.position_type =\'2\' THEN \'空\' \
					ELSE t.position_type END \'方向\',\
					t.current_amount \'数量\', \
					tf.fund_code \'产品代码\', \
					tf.fund_name \'产品名称\', \
					tca.broker_name \'期货公司\', \
					tca.capital_account_no \'资金账号\'  \
				FROM \
					tunitstock t, \
					tfuturekind tfk, \
					tstockinfo_future tsf, \
					tfund tf, \
					tasset ta, \
					tassetcapital tac, \
					tcapitalaccount tca  \
				WHERE \
					t.report_code = tsf.report_code  \
					AND tsf.future_kind_id = tfk.future_kind_id  \
					AND t.business_date = {0}  \
					AND UPPER( t.report_code ) = \'{1}\'  \
					AND t.market_no IN ( \'3\', \'4\', \'7\', \'9\', \'34\' )  \
					AND t.position_type = \'{2}\'  \
					AND t.current_amount > 0  \
					AND t.asset_id = ta.asset_id  \
					AND tf.fund_id = ta.fund_id  \
					AND ta.asset_id = tac.asset_id  \
					AND tca.capital_account_id = tac.capital_account_id  \
				ORDER BY t.current_amount DESC;'.format(business_date, report_code, position_type)
				logger.debug('select sql: ' + sql)
				cursor.execute(sql)
				if not is_title_filled:
					for field_desc in cursor.description:
						title.append(field_desc[0])
					detail_data.append(tuple(title))
					is_title_filled = True
				data = cursor.fetchall()
				for i in range(0, len(data)):
					detail_data.append(data[i])
			logger.debug('[detail_data]:{0}'.format(detail_data))
			return detail_data
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))
			raise e
		finally:
			cursor.close()
			mysql_conn.close()

# 明细持仓数据加上产品信息
## 输入格式：business_date, position_type, report_code, current_amount, fund_code, fund_name, broker_name, capital_account_no
## 返回格式：
def GetFundInfo(I_data):
	for i in range(0, len(I_data)):
		fund_id = I_data[i][4]
		one_data = I_data[i]
		try:
			mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
										 user='trader', password='123456',
										 db='MailSaver',
										 charset='utf8')
		except Exception as e:
			logger.error("mysql connect fail: {0}".format(e))
			raise e
		else:
			cursor = mysql_conn.cursor()
			try:
				sql = ''
			except Exception as e:
				logger.error("Sql execute error: {0}".format(e))
				raise e
			finally:
				cursor.close()
				mysql_conn.close()

# 市场数据进入market_holding表，持仓数据进入company_holding表
# 表数据整理后写入Excel
def MergeDataIntoExcel(market_insert_sql, holding_insert_sql, path):
	EXCEL_NAME = '期货持仓占比概况'
	SUFFIX_NAME = '.xlsx'
	save_file = os.path.join(path, HQ_DATE_OPLUS + EXCEL_NAME + SUFFIX_NAME)
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
			# wind进入market_holding表，Oplus进入company_holding表
			if market_insert_sql != '':
				try:
					sql = 'DELETE FROM market_holding2 WHERE business_date = \'{0}\';'.format(HQ_DATE_OPLUS)
					logger.debug('delete sql: ' + sql)
					cursor.execute(sql)
					mysql_conn.commit()
					logger.debug("insert sql: " + market_insert_sql)
					cursor.execute(market_insert_sql)
					mysql_conn.commit()
				except Exception as e:
					logger.error("Sql execute error: {0}".format(e))
			if holding_insert_sql != '':
				try:
					sql = 'DELETE FROM company_holding2 WHERE business_date = \'{0}\';'.format(HQ_DATE_OPLUS)
					logger.debug('delete sql: ' + sql)
					cursor.execute(sql)
					mysql_conn.commit()
					logger.debug("insert sql: " + holding_insert_sql)
					cursor.execute(holding_insert_sql)
					mysql_conn.commit()
				except Exception as e:
					logger.error("Sql execute error: {0}".format(e))

			# 数据整理后进入临时表
			# 合约临时表
			sql = 'CREATE TEMPORARY TABLE holding_detail( \
					`business_date` VARCHAR(20), \
					`position_type` VARCHAR(20), \
					`report_code` VARCHAR(20), \
					`future_kind_code` VARCHAR(20), \
					`current_amount` DOUBLE(20, 4), \
					`position_quantity` DOUBLE(20, 4), \
					`share` VARCHAR(20) \
					);';
			logger.debug('creat temp table sql: ' + sql)
			cursor.execute(sql)
			mysql_conn.commit()
			sql = 'INSERT INTO holding_detail(business_date, position_type, report_code, future_kind_code, current_amount, position_quantity, `share`) \
				SELECT \
					t.business_date, \
					t.position_type, \
					t.report_code, \
					t.future_kind_code, \
					t.current_amount, \
					m.position_quantity, \
					concat( round( t.current_amount / m.position_quantity * 100, 2 ), \'%\' ) `share` \
				FROM \
					( \
				SELECT \
					tm.business_date, \
					tm.report_code, \
					tm.position_quantity, \
					tm.future_kind_code \
				FROM \
					market_holding2 tm  \
				WHERE \
					tm.business_date = \'{0}\'  \
					) m \
					RIGHT JOIN ( \
				SELECT \
					tc.business_date, \
					tc.position_type, \
					tc.report_code, \
					tc.future_kind_code, \
					tc.current_amount  \
				FROM \
					company_holding2 tc  \
				WHERE \
					tc.business_date = \'{0}\'  \
					) t ON m.report_code = t.report_code \
					AND t.business_date = m.business_date  \
				ORDER BY \
					t.position_type, \
					t.report_code;'.format(HQ_DATE_OPLUS)
			logger.debug('insert sql: ' + sql)
			cursor.execute(sql)
			mysql_conn.commit()
			#品种临时表
			sql = 'CREATE TEMPORARY TABLE holding_gathering( \
					`business_date` VARCHAR(20), \
					`position_type` VARCHAR(20), \
					`future_kind_code` VARCHAR(20), \
					`current_amount` DOUBLE(20, 4), \
					`position_quantity` DOUBLE(20, 4), \
					`share` VARCHAR(20) \
					);'
			logger.debug('creat temp table sql: ' + sql)
			cursor.execute(sql)
			mysql_conn.commit()
			sql = 'INSERT INTO holding_gathering(business_date, future_kind_code, position_type, current_amount, position_quantity, `share`) \
				SELECT \
				t.business_date, \
				t.future_kind_code, \
				t.position_type, \
				t.current_amount, \
				m.position_quantity, \
				concat( round( t.current_amount / m.position_quantity * 100, 2 ),\'%\' ) `share`  \
			FROM \
				( \
			SELECT \
				tmf.business_date, \
				UPPER( tmf.future_kind_code ) future_kind_code, \
				sum( tmf.position_quantity ) position_quantity  \
			FROM \
				( \
			SELECT \
				tm.business_date, \
				tm.report_code, \
				tm.position_quantity, \
				tm.future_kind_code \
			FROM \
				market_holding2 tm  \
			WHERE \
				tm.business_date =\'{0}\'  \
				) tmf  \
			GROUP BY \
				tmf.business_date, \
				tmf.future_kind_code  \
				) m RIGHT JOIN  \
				( \
			SELECT \
				tc.business_date, \
				tc.future_kind_code, \
				tc.position_type, \
				sum( tc.current_amount ) current_amount  \
			FROM \
				company_holding2 tc  \
			WHERE \
				tc.business_date =\'{0}\'  \
			GROUP BY \
				tc.business_date, \
				tc.future_kind_code, \
			tc.position_type	 \
				) t \
				ON m.future_kind_code = t.future_kind_code;'.format(HQ_DATE_OPLUS)
			logger.debug('insert sql: ' + sql)
			cursor.execute(sql)
			mysql_conn.commit()
			#临时表联合查询
			sql = 'SELECT \
				CASE  \
				WHEN d.position_type =\'1\' THEN \
				\'多\'  \
				WHEN d.position_type =\'2\' THEN \
				\'空\' \
				ELSE d.position_type  \
				END \'方向\', \
				d.future_kind_code \'品种\', \
				g.current_amount \'公司品种持仓量\', \
				g.position_quantity \'市场品种单边持仓量\', \
				g.`share` \'占比\', \
				d.report_code \'合约\', \
				d.current_amount \'合约公司持仓量\', \
				d.position_quantity \'合约市场单边持仓量\', \
				d.`share` \'占比\' \
			FROM \
				holding_detail d \
				LEFT JOIN holding_gathering g ON d.position_type = g.position_type  \
				AND d.future_kind_code = g.future_kind_code  \
			ORDER BY \
				d.position_type, \
				d.future_kind_code, \
				d.report_code;'
			logger.debug('select sql: ' + sql)
			cursor.execute(sql)
			#标题加到数据中
			gather_data = []
			title = []
			for field_desc in cursor.description:
				title.append(field_desc[0])
			gather_data.append(tuple(title))
			for row in cursor.fetchall():
				gather_data.append(row)
			logger.debug('data is: {0}'.format(gather_data))

			#整理看是否有超过20%的品种，如果有，要把明细数据写在新的Excel中
			sql = 'SELECT \
					t.business_date, \
					t.position_type, \
					t.report_code \
				FROM \
					holding_detail t  \
				WHERE \
					t.business_date = {0}  \
					AND CONVERT ( LEFT ( t.`share`, LENGTH( t.`share` ) - 1 ), SIGNED ) >= 20'.format(HQ_DATE_OPLUS)
			logger.debug('select sql: ' + sql)
			cursor.execute(sql)
			select_data = cursor.fetchall();
			if (len(select_data) > 0):
				detail_data = GetHoldingDetail(select_data)
				namelist = ('公司持仓总览', '20%预警明细数据')
				datalist = []
				datalist.append(gather_data)
				datalist.append(detail_data)
				logger.debug('[namelist]:{0}'.format(namelist))
				logger.debug('[datalist]:{0}'.format(datalist))
				dunhe_public.WriteMultiData2Excel(save_file, namelist, datalist)
			else:
				dunhe_public.WriteData2Excel(gather_data, save_file)
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))
			raise e
		finally:
			cursor.close()
			mysql_conn.close()
	return save_file


# 主变量
#日志
logger = dunhe_public.SetLog('HoldingShareFromMarket')
# 读取哪天的行情
HQ_DATE_OPLUS = datetime.datetime.now().strftime("%Y%m%d")
HQ_DATE_OPLUS = '20190227'
# 文件保存位置
SAVE_PATH = "G:\\data"
ESCAPE_SENDING = 1 #0-发送，1-不发送
RECIEVE_LIST=['gaos@dunhefund.com', 'tanghj@dunhefund.com', 'panhm@dunhefund.com']

file = MergeDataIntoExcel(GetMarketData(), GetHoldingData(), SAVE_PATH)
if not ESCAPE_SENDING and file != '':
	dunhe_public.SendingMailFromIT(RECIEVE_LIST, '', '', file)