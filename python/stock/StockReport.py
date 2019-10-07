#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import cx_Oracle
import os
import datetime
import re
import xlrd
import openpyxl
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

######################################################################################
# Step 1 估值表数据读取
######################################################################################

def GetNetTableData(date = ''):
	if date == '':
		date = dunhe_public.GetTradedate(datetime.datetime.now().strftime("%Y%m%d"), DAY_DIFF)
	logger.info("Get Nettable[{0}]".format(date))

	try:
		connection = pymysql.connect(host='192.168.40.202', port=3306,
									 user='trader', password='123456',
									 db='MailSaver',
									 charset='utf8')
	except Exception as e:
		logger.error("Sever connect fail: {0}".format(e))
		return (False, [])
	else:
		cursor = connection.cursor()
		sql_fundinfo = "SELECT t.FundCode, t.FundName, t.Remark from FundInfo_ALL t WHERE POSITION(\'User:\' in t.Remark) > 0 and POSITION(\'LWL\' in t.Remark) > 0 and Valid = \'1\';"
		try:
			#先从Mysql中把要核对的产品取出来
			logger.debug('select sql: ' + sql_fundinfo)
			cursor.execute(sql_fundinfo)
			fundinfo = cursor.fetchall()
			logger.debug("Fund info: {0}".format(fundinfo))
			#关闭数据库
			cursor.close()
			connection.close()
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))
			return (False, [])

		listfundinfo = []
		dictfundname = {}
		allfundcode = ''
		for fundcode, fundname, remark in fundinfo:
			fundcodes_in_one_fund = '|' + fundcode
			if remark.find('Fundcode:') >= 0:
				fundrenamesplit = remark.split('Fundcode:')
				if (fundrenamesplit[1].find(',') >= 0):
					fundrenames = fundrenamesplit[1].split(',')
					for fundrename in fundrenames:
						dictfundname[fundrename] = fundcode
						fundcodes_in_one_fund = fundcodes_in_one_fund + '|' + fundrename
				else:
					dictfundname[fundrenamesplit[1]] = fundcode
					fundcodes_in_one_fund = fundcodes_in_one_fund + '|' + fundrenamesplit[1]
			allfundcode = allfundcode + fundcodes_in_one_fund
			listfundinfo.append([fundcodes_in_one_fund + '|', fundname, 0])
		logger.debug(listfundinfo)
		allfundcode = allfundcode + '|'
		logger.debug("All funds code: " + allfundcode)
		logger.debug("fundname dict: {0}".format(dictfundname))

		net_info_sql = 'SELECT \
						to_char ( D_FILEDATE, \'YYYYMMDD\' ) funddate, \
						VC_ZHCODE fundcode, \
						VC_FKMBM subcode, \
						VC_FKMMC subname  \
					FROM \
						GZ_FUND_GZB  \
					WHERE \
						D_FILEDATE = TO_DATE ( \'{0}\', \'YYYYMMDD\' )  \
						AND instr(\'{1}\', concat( concat( \'|\', VC_ZHCODE ), \'|\' )) > 0  \
						AND ( VC_FKMBM LIKE \'1102%\' OR VC_FKMBM LIKE \'1103%\' )  \
						AND vc_mkt_code IS NOT NULL UNION ALL \
					SELECT \
						to_char ( D_BIZ, \'YYYYMMDD\' ) funddate, \
						VC_ZHCODE fundcode, \
						vc_subj_code subcode, \
						vc_subj_name subname  \
					FROM \
						GZ_PRD_GZB  \
					WHERE \
						D_BIZ = TO_DATE ( \'{0}\', \'YYYYMMDD\' )  \
						AND instr(\'{1}\', concat( concat( \'|\', VC_ZHCODE ), \'|\' )) > 0  \
						AND ( vc_subj_code LIKE \'1102.%\' OR vc_subj_code LIKE \'1103.%\' )  \
						AND vc_mkt_code IS NOT NULL  \
					ORDER BY \
						fundcode, \
						subcode'.format(date, allfundcode)
		try:
			tns = cx_Oracle.makedsn('192.168.40.73',1521,'orcl')
			oracle_conn = cx_Oracle.connect('gaos','oplus',tns)
		except Exception as e:
			logger.error("oracle connect fail: {0}".format(e))
			return (False, [])
		else:
			cursor = oracle_conn.cursor()
			logger.debug('select sql: ' + net_info_sql)
			try:
				cursor.execute(net_info_sql)
				subdata = cursor.fetchall()
			except Exception as e:
				logger.debug("Sql execute error: {0}".format(e))
				return (False, [])
			else:
				listsubdata = []
				for funddate, fundcode, subcode, subname in subdata:
					for i in range (0, len(listfundinfo)):
						if listfundinfo[i][0].find('|' + fundcode + '|') >= 0:
							listfundinfo[i][2] = 1
							fundname = listfundinfo[i][1]
					if subcode.find("1102") == 0:
						subtype = "股票"
					elif subcode.find("1103") == 0:
						# 1103.04 上海可转债；110312 上海可转债
						if subcode.find("1103.04") == 0 or subcode.find("110312"):
							subtype = "可转债"
						# 1103.61 深圳可转债；110332 深圳可转债
						elif subcode.find("1103.61") == 0 or subcode.find("110332"):
							subtype = "可转债"
						# 1103.02 上海企业债
						elif subcode.find("1103.02") == 0:
							subtype = "企业债"
						# 1103.03 上海公司债
						elif subcode.find("1103.03") == 0:
							subtype = "公司债"
						else:
							subtype = "债券"
					else:
						subtype = "其他"
					if (fundcode in dictfundname):
						fundcode = dictfundname[fundcode]
					listsubdata.append([funddate, fundcode, fundname, subcode, subname, subtype])
		finally:
			cursor.close()
			oracle_conn.close()
	logger.debug("Subject detail: {0}".format(listsubdata))

	iSuccess = 0
	for fundcode, fundname, result in listfundinfo:
		if result == 1:
			iSuccess += 1
			logger.info("Fund[{0}]{1} get subject data successfully".format(fundcode, fundname))
		else:
			logger.info("Fund[{0}]{1} get subject data fail".format(fundcode, fundname))
	logger.info("Get subject data success[{0}] fail[{1}] total[{2}]".format(iSuccess, len(listfundinfo) - iSuccess, len(listfundinfo)))
	return (True, listsubdata)


######################################################################################
# Step 2 把股票数据存入数据库
######################################################################################

def GetStockIntoDB2(listsubdata):
	if listsubdata:
		date = listsubdata[0][0]

	try:
		connection = pymysql.connect(host='192.168.40.202', port=3306,
									 user='trader', password='123456',
									 db='MailSaver',
									 charset='utf8')
	except Exception as e:
		logger.error("Sever connect fail: {0}".format(e))
		return False
	else:
		cursor = connection.cursor()
		sql = 'delete from StockHoldingDetail where tradedate = {0};'.format(date)
		logger.debug('delete sql: ' + sql)
		cursor.execute(sql)
		connection.commit()
		
		for funddate, fundcode, fundname, subcode, subname, subtype in listsubdata:
			sql = 'INSERT INTO StockHoldingDetail VALUES(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\');'.format(\
						funddate, fundname, fundcode, subcode, subname, subtype)
			logger.debug('insert sql:' + sql)
			try:
				cursor.execute(sql)
				connection.commit()
				logger.debug("Successfully insert StockHoldingDetail: code[{0}] name[{1}] subject[{2}] data[{3}] type[{4}] date[{5}]".format(\
							fundcode, fundname, subcode, subname, subtype, funddate))
			except Exception as e:
				logger.error("insert execute error: {0}".format(e))

		# 关闭数据库
		cursor.close()
		connection.close()
	return True


######################################################################################
#Step 3 整理数据，输出成excel
######################################################################################

def OutPutExcelFile():
	save_file = ''
	report_data = []
	EXCEL_NAME = '公司股票持仓概况'
	SUFFIX_NAME = '.xlsx'
	try:
		connection = pymysql.connect(host='192.168.40.202', port=3306,
									 user='trader', password='123456',
									 db='MailSaver',
									 charset='utf8')
	except Exception as e:
		logger.error("Sever connect fail: {0}".format(e))
	else:
		cursor = connection.cursor()
		try:
			# 把StockHoldingDetail明细数据整理进入HoldingMerge
			if DEST_DIR_DATE == '':		
				sql_code = 'SELECT max(t.tradedate) tradedate from StockHoldingDetail t;'
				logger.debug('select sql: ' + sql_code)
				cursor.execute(sql_code)
				s_tradedate = cursor.fetchone()[0]
				logger.debug('select result: {0}'.format(s_tradedate))
			else:
				s_tradedate = DEST_DIR_DATE
			logger.info('HoldingMerge resort from date ' + s_tradedate)
			#先删除HoldingMerge当天数据
			sql_code = 'DELETE FROM HoldingMerge WHERE TradeDate = \'{0}\';'.format(s_tradedate);
			logger.debug('delete sql: ' + sql_code)
			cursor.execute(sql_code)
			connection.commit()
			#重新插入整理后的数据
			sql_code = 'INSERT INTO HoldingMerge SELECT\
				a.TradeDate,\
				min( a.stockcode ) stockcode,\
				a.stockname,\
				a.Manager, \
				\'0\' windcode, \
				a.type \
				FROM\
					(\
				SELECT\
					t.TradeDate,\
					min( t.stockcode ) stockcode,\
					t.stockname,\
					t.type,\
					tf.Manager \
				FROM\
					StockHoldingDetail t,\
					FundInfo_ALL tf \
				WHERE\
					LENGTH( t.stockcode ) > 10 \
					AND tf.FundCode = t.fundcode \
					AND t.tradedate = \'{0}\' \
					AND INSTR( tf.Manager, \'|\' ) = 0 \
				GROUP BY\
					tf.manager,\
					t.tradedate,\
					t.type,\
					t.stockname UNION\
				SELECT\
					t.TradeDate,\
					min( t.stockcode ) stockcode,\
					t.stockname,\
					t.type, \
					SUBSTR( tf.Manager, 1, INSTR( tf.Manager, \'|\' ) - 1 ) Manager \
				FROM\
					StockHoldingDetail t,\
					FundInfo_ALL tf \
				WHERE\
					LENGTH( t.stockcode ) > 10 \
					AND tf.FundCode = t.fundcode \
					AND t.tradedate = \'{0}\' \
					AND INSTR( tf.Manager, \'|\' ) > 0 \
				GROUP BY\
					tf.manager,\
					t.tradedate,\
					t.type, \
					t.stockname UNION\
				SELECT\
					t.TradeDate,\
					min( t.stockcode ) stockcode,\
					t.stockname,\
					t.type, \
					SUBSTR(\
					tf.Manager,\
					INSTR( tf.Manager, \'|\' ) + 1,\
					LENGTH( tf.Manager ) - INSTR( tf.Manager, \'|\' ) \
					) Manager \
				FROM\
					StockHoldingDetail t,\
					FundInfo_ALL tf \
				WHERE\
					LENGTH( t.stockcode ) > 10 \
					AND tf.FundCode = t.fundcode \
					AND t.tradedate = \'{0}\' \
					AND INSTR( tf.Manager, \'|\' ) > 0 \
				GROUP BY\
					tf.manager,\
					t.tradedate,\
					t.type, \
					t.stockname \
					) a \
				GROUP BY\
					a.TradeDate,\
					a.stockname,\
					a.type, \
					a.Manager;'.format(s_tradedate)
			logger.debug('insert sql: ' + sql_code)
			cursor.execute(sql_code)
			connection.commit()

			# 把HoldingMerge的代码整理成Wind可以识别的
			sql_code = 'UPDATE HoldingMerge t set t.windcode = CASE \
			WHEN INSTR(t.stockcode,\'.\') > 0 THEN  \
				CASE \
					WHEN INSTR(t.stockcode, \' SH\') > 0 THEN \
						CONCAT(SUBSTRING_INDEX(SUBSTRING_INDEX(t.stockcode, \'.\', -1), \' \', 1), \'.SH\') \
					WHEN INSTR(t.stockcode, \' SZ\') > 0 THEN \
						CONCAT(SUBSTRING_INDEX(SUBSTRING_INDEX(t.stockcode, \'.\', -1), \' \', 1), \'.SZ\') \
					WHEN INSTR(t.stockcode, \' HG\') > 0 THEN \
						CONCAT(RIGHT(SUBSTRING_INDEX(SUBSTRING_INDEX(t.stockcode, \'.\', -1), \' \', 1), 4), \'.HK\') \
					WHEN INSTR(t.stockcode, \' HS\') > 0 THEN \
						CONCAT(RIGHT(SUBSTRING_INDEX(SUBSTRING_INDEX(t.stockcode, \'.\', -1), \' \', 1), 4), \'.HK\') \
					WHEN INSTR(t.stockcode, \' OTC\') > 0 THEN \
						CONCAT(SUBSTRING_INDEX(SUBSTRING_INDEX(t.stockcode, \'.\', -1), \' \', 1), \'.OF\') \
					ELSE \
						t.stockcode \
				END \
			ELSE \
				CASE \
					WHEN INSTR(t.stockcode, \'110201\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SH\') \
					WHEN INSTR(t.stockcode, \'110203\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SH\') \
					WHEN INSTR(t.stockcode, \'110231\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SZ\') \
					WHEN INSTR(t.stockcode, \'110233\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SZ\') \
					WHEN INSTR(t.stockcode, \'110241\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SZ\') \
					WHEN INSTR(t.stockcode, \'110246\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SZ\') \
					WHEN INSTR(t.stockcode, \'110281\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 4), \'.HK\') \
					WHEN INSTR(t.stockcode, \'110282\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 4), \'.HK\') \
					WHEN INSTR(t.stockcode, \'110312\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SH\') \
					WHEN INSTR(t.stockcode, \'110332\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.SZ\') \
					WHEN INSTR(t.stockcode, \'110502\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.OF\') \
					WHEN INSTR(t.stockcode, \'110503\') > 0 THEN \
						CONCAT(RIGHT(t.stockcode, 6), \'.OF\') \
					ELSE \
						t.stockcode \
				END \
			END \
			WHERE t.tradedate = \'{0}\' ;'.format(s_tradedate)
			logger.debug('update sql: ' + sql_code)
			cursor.execute(sql_code)
			connection.commit()

			# 对比两天数据，形成增删改记录
			sql_code = 'SELECT t.tradedate FROM HoldingMerge t WHERE t.tradedate <= \'{0}\' GROUP BY t.tradedate ORDER BY t.tradedate DESC LIMIT 2;'.format(s_tradedate)
			logger.debug('select sql: ' + sql_code)
			cursor.execute(sql_code)
			tradedate_top2 = cursor.fetchall()
			if len(tradedate_top2) == 2:
				tradedate_today = tradedate_top2[0][0]
				tradedate_yes = tradedate_top2[1][0]
				logger.info('compare date {0} {1}'.format(tradedate_today, tradedate_yes))
				sql_code = 'SELECT distinct \
								m.tradedate1 \'交易日1\', \
								m.tradedate2 \'交易日2\', \
							CASE \
								WHEN m.windcode1 IS NULL THEN \
								m.windcode2 ELSE m.windcode1  \
								END \'股票代码\', \
							CASE \
								WHEN m.stockname1 IS NULL THEN \
								m.stockname2 ELSE m.stockname1  \
								END \'股票简称\', \
							CASE \
								WHEN m.type1 IS NULL THEN \
								m.type2 ELSE m.type1  \
								END \'证券类别\', \
								m.manager \'基金经理\', \
							CASE \
								WHEN m.windcode1 is NULL THEN \
									\'Add\' \
								WHEN m.windcode2 is NULL THEN \
									\'Delete\' \
								ELSE \
									\'Stay\' \
							END \'持仓状态\' \
							FROM \
								( \
							SELECT \
								a.tradedate tradedate1, \
								b.tradedate tradedate2, \
								a.windcode windcode1, \
								b.windcode windcode2, \
								a.stockname stockname1, \
								b.stockname stockname2, \
								a.type type1, \
								b.type type2, \
								a.manager \
							FROM \
								( SELECT * FROM HoldingMerge t1 WHERE t1.tradedate = \'{0}\' ) a \
								LEFT JOIN ( SELECT * FROM HoldingMerge t2 WHERE t2.tradedate = \'{1}\' ) b ON a.windcode = b.windcode  \
								AND a.manager = b.manager UNION \
							SELECT \
								a.tradedate tradedate1, \
								b.tradedate tradedate2, \
								a.windcode windcode1, \
								b.windcode windcode2, \
								a.stockname stockname1, \
								b.stockname stockname2, \
								a.type type1, \
								b.type type2, \
								b.manager  \
							FROM \
								( SELECT * FROM HoldingMerge t1 WHERE t1.tradedate = \'{0}\' ) a \
								RIGHT JOIN ( SELECT * FROM HoldingMerge t2 WHERE t2.tradedate = \'{1}\' ) b ON a.windcode = b.windcode  \
								AND a.manager = b.manager  \
								) m'.format(tradedate_yes, tradedate_today)
				logger.debug('select sql: ' + sql_code)
				cursor.execute(sql_code)
				title = []
				for field_desc in cursor.description:
					title.append(field_desc[0])
				report_data.append(tuple(title))
				for row in cursor.fetchall():
					report_data.append(row)
				logger.debug('Report dats is: {0}'.format(report_data))
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))

	# 关闭数据库
	cursor.close()
	connection.close()

	#导出到excel中
	save_file = os.path.join(SAVE_PATH, tradedate_today + EXCEL_NAME + SUFFIX_NAME)
	dunhe_public.WriteData2Excel(report_data, save_file)
	return save_file


# 主变量
#日志
logger = dunhe_public.SetLog('StockReport')
# 文件保存位置
SAVE_PATH = "G:\\data\\stockreport"
# 读取哪天的估值文件
DEST_DIR_DATE = ""
#DEST_DIR_DATE = "20190311"
DAY_DIFF = -2
# 跳过发送邮件 0-不跳过 1-跳过
ESCAPE_SENDING = 0
#RECEIVER_LIST = ['gaos@dunhefund.com']
RECEIVER_LIST = ['liwl@dunhefund.com', 'wangcy@dunhefund.com', 'zhangzz@dunhefund.com', 'gaos@dunhefund.com']

# 1 获取数据
result = GetNetTableData(DEST_DIR_DATE)
if result[0]:
# 2 估值数据进入数据库
	if GetStockIntoDB2(result[1]):
# 3 生成对比文件		
		file = OutPutExcelFile()
#4 发送邮件
		if not ESCAPE_SENDING:
			dunhe_public.SendingMailFromIT(RECEIVER_LIST, '', '', file)

