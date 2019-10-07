# -*- condig: utf-8 -*-

import pymysql
import cx_Oracle
import os
import logging
import datetime
import xlrd
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

# startdate, enddate 格式YYYYMMDD，日期头尾都包含
# fundcode是以','为分隔符的字符串，例如'S1,S2'
def GetNetValue(I_startdate = '', I_enddate = '', I_fundcode = ''):
	sql = 'SELECT \
				to_char(D_FDATE, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_FKMBM subname, to_number(VC_FKMMC) netval FROM GZ_FUND_GZB \
			WHERE 1 = 1 \
				AND (VC_FKMBM = \'基金单位净值：\' OR VC_FKMBM = \'今日单位净值：\') \
				{0} \
			UNION ALL \
			SELECT to_char(D_BIZ, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_KEY_NAME subname, F_VALRATE netval FROM GZ_PRD_GZB  \
			WHERE 1 =1 \
				and VC_KEY_NAME like \'今日单位净值%\' \
				{1} '
	sql_date0 = ''
	sql_date1 = ''
	if I_startdate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE >= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_startdate)
		sql_date1 = sql_date1 + ' and D_BIZ >= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_startdate)
	if I_enddate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE <= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_enddate)
		sql_date1 = sql_date1 + ' and D_BIZ <= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_enddate)
	if I_fundcode != '':
		sql_fundcode = ' and VC_ZHCODE in (\'' + I_fundcode.replace(',', '\',\'') + '\')'
	else:
		sql_fundcode = ''
	sql = sql.format(sql_date0 + sql_fundcode, sql_date1 + sql_fundcode)

	try:
		tns = cx_Oracle.makedsn('192.168.40.73',1521,'orcl')
		oracle_conn = cx_Oracle.connect('gaos','oplus',tns)
	except Exception as e:
		logger.error("oracle connect fail: {0}".format(e))
		return (False, [])
	else:
		cursor = oracle_conn.cursor()
		logger.debug('select sql: ' + sql)
		try:
			cursor.execute(sql)
			netdata = cursor.fetchall()
			logger.debug('net value result: {0}'.format(netdata))
		except Exception as e:
			logger.debug("Sql execute error: {0}".format(e))
			return (False, [])
		else:
			return (True, netdata)
	finally:
		cursor.close()
		oracle_conn.close()

def GetNetAssetValue(I_startdate = '', I_enddate = '', I_fundcode = ''):
	sql = 'SELECT to_char(D_FDATE, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_FKMBM subname, F_FZQSZ net_asset FROM GZ_FUND_GZB \
			WHERE 1 = 1 \
			AND VC_FKMBM = \'基金资产净值:\' \
			{0} \
			UNION ALL \
			SELECT to_char(D_BIZ, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_KEY_NAME subname, F_HLDMKV_LOCL net_asset FROM GZ_PRD_GZB \
			WHERE 1 = 1 \
 			and VC_KEY_NAME like \'资产净值%\' \
			{1} '
	sql_date0 = ''
	sql_date1 = ''
	if I_startdate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE >= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_startdate)
		sql_date1 = sql_date1 + ' and D_BIZ >= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_startdate)
	if I_enddate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE <= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_enddate)
		sql_date1 = sql_date1 + ' and D_BIZ <= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_enddate)
	if I_fundcode != '':
		sql_fundcode = ' and VC_ZHCODE in (\'' + I_fundcode.replace(',', '\',\'') + '\')'
	else:
		sql_fundcode = ''
	sql = sql.format(sql_date0 + sql_fundcode, sql_date1 + sql_fundcode)

	try:
		tns = cx_Oracle.makedsn('192.168.40.73',1521,'orcl')
		oracle_conn = cx_Oracle.connect('gaos','oplus',tns)
	except Exception as e:
		logger.error("oracle connect fail: {0}".format(e))
		return (False, [])
	else:
		cursor = oracle_conn.cursor()
		logger.debug('select sql: ' + sql)
		try:
			cursor.execute(sql)
			netdata = cursor.fetchall()
			logger.debug('net value result: {0}'.format(netdata))
		except Exception as e:
			logger.debug("Sql execute error: {0}".format(e))
			return (False, [])
		else:
			return (True, netdata)
	finally:
		cursor.close()
		oracle_conn.close()

def GetTotalAssetValue(I_startdate = '', I_enddate = '', I_fundcode = ''):
	sql = 'SELECT to_char(D_FDATE, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_FKMBM subname, F_FZQSZ total_asset FROM GZ_FUND_GZB \
			WHERE 1 = 1 \
			AND VC_FKMBM = \'资产类合计:\' \
			{0} \
			UNION ALL \
			SELECT to_char(D_BIZ, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_KEY_NAME subname, F_HLDMKV_LOCL total_asset FROM GZ_PRD_GZB \
			WHERE 1 = 1 \
 			and VC_KEY_NAME like \'资产合计%\' \
			{1} '
	sql_date0 = ''
	sql_date1 = ''
	if I_startdate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE >= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_startdate)
		sql_date1 = sql_date1 + ' and D_BIZ >= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_startdate)
	if I_enddate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE <= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_enddate)
		sql_date1 = sql_date1 + ' and D_BIZ <= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_enddate)
	if I_fundcode != '':
		sql_fundcode = ' and VC_ZHCODE in (\'' + I_fundcode.replace(',', '\',\'') + '\')'
	else:
		sql_fundcode = ''
	sql = sql.format(sql_date0 + sql_fundcode, sql_date1 + sql_fundcode)

	try:
		tns = cx_Oracle.makedsn('192.168.40.73',1521,'orcl')
		oracle_conn = cx_Oracle.connect('gaos','oplus',tns)
	except Exception as e:
		logger.error("oracle connect fail: {0}".format(e))
		return (False, [])
	else:
		cursor = oracle_conn.cursor()
		logger.debug('select sql: ' + sql)
		try:
			cursor.execute(sql)
			netdata = cursor.fetchall()
			logger.debug('net value result: {0}'.format(netdata))
		except Exception as e:
			logger.debug("Sql execute error: {0}".format(e))
			return (False, [])
		else:
			return (True, netdata)
	finally:
		cursor.close()
		oracle_conn.close()

def GetCashAssetValue(I_startdate = '', I_enddate = '', I_fundcode = ''):
	sql = 'SELECT to_char(D_FDATE, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_FKMBM subname, F_FZQSZ cash_asset, 0 cash_share FROM GZ_FUND_GZB a \
			WHERE 1 = 1 \
				AND VC_FKMBM LIKE \'现金类资产%\' AND not EXISTS (SELECT 1 FROM GZ_FUND_GZB b WHERE a.D_FDATE = b.D_FDATE and a.VC_ZHCODE = b.VC_ZHCODE AND b.VC_FKMBM like \'现金类占净值比%\') \
				{0} \
			UNION ALL \
			SELECT to_char(D_FDATE, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_FKMBM subname, 0 cash_asset, to_number(vc_FKMMC) cash_share FROM GZ_FUND_GZB a \
			WHERE 1 = 1 \
				AND VC_FKMBM LIKE \'现金类占净值比%\' AND not EXISTS (SELECT 1 FROM GZ_FUND_GZB b WHERE a.D_FDATE = b.D_FDATE and a.VC_ZHCODE = b.VC_ZHCODE AND b.VC_FKMBM like \'现金类资产%\') \
				{0} \
			UNION ALL \
			SELECT to_char(D_FDATE, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_FKMBM subname, F_FZQSZ cash_asset, 0 cash_share FROM GZ_FUND_GZB a \
			WHERE 1 = 1 \
				AND VC_FKMBM LIKE \'现金类资产%\' AND EXISTS (SELECT 1 FROM GZ_FUND_GZB b WHERE a.D_FDATE = b.D_FDATE and a.VC_ZHCODE = b.VC_ZHCODE AND b.VC_FKMBM like \'现金类占净值比%\') \
				{0} \
			UNION ALL \
			SELECT to_char(D_BIZ, \'yyyymmdd\') funddate, VC_ZHCODE fundcode, VC_KEY_NAME subname, 0 cash_asset, F_VALRATE cash_share FROM GZ_PRD_GZB  \
			WHERE 1 =1 \
			 and VC_KEY_NAME like \'现金类占净值比%\' \
			 {1} '
	sql_date0 = ''
	sql_date1 = ''
	if I_startdate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE >= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_startdate)
		sql_date1 = sql_date1 + ' and D_BIZ >= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_startdate)
	if I_enddate != '':
		sql_date0 = sql_date0 + ' AND D_FDATE <= to_date ( \'{0} 00:00:00\', \'yyyymmdd hh24:mi:ss\' )'.format(I_enddate)
		sql_date1 = sql_date1 + ' and D_BIZ <= to_date ( \'{0} 00:00:00\', \'yyyy-mm-dd hh24:mi:ss\' )'.format(I_enddate)
	if I_fundcode != '':
		sql_fundcode = ' and VC_ZHCODE in (\'' + I_fundcode.replace(',', '\',\'') + '\')'
	else:
		sql_fundcode = ''
	sql = sql.format(sql_date0 + sql_fundcode, sql_date1 + sql_fundcode)

	try:
		tns = cx_Oracle.makedsn('192.168.40.73',1521,'orcl')
		oracle_conn = cx_Oracle.connect('gaos','oplus',tns)
	except Exception as e:
		logger.error("oracle connect fail: {0}".format(e))
		return (False, [])
	else:
		cursor = oracle_conn.cursor()
		logger.debug('select sql: ' + sql)
		try:
			cursor.execute(sql)
			netdata = cursor.fetchall()
			logger.debug('net value result: {0}'.format(netdata))
		except Exception as e:
			logger.debug("Sql execute error: {0}".format(e))
			return (False, [])
		else:
			return (True, netdata)
	finally:
		cursor.close()
		oracle_conn.close()

def GetValue(I_startdate = '', I_enddate = '', I_fundcode = ''):
	# 格式： [0]date, [1]fundcode, [2]netvalue, [3]netasset, [4]totalasset, [5]cashasset
	netlist = []

	result = GetNetValue(I_startdate, I_enddate, I_fundcode)
	if result[0]:
		for funddate, fundcode, subname, netvalue in result[1]:
			netlist.append([funddate, fundcode, netvalue, 0, 0, 0])

	result = GetNetAssetValue(I_startdate, I_enddate, I_fundcode)
	if result[0]:
		for funddate, fundcode, subname, netasset in result[1]:
			for i in range(0, len(netlist)):
				if funddate == netlist[i][0] and fundcode == netlist[i][1]:
					netlist[i][3] = netasset

	result = GetTotalAssetValue(I_startdate, I_enddate, I_fundcode)
	if result[0]:
		for funddate, fundcode, subname, totalasset in result[1]:
			for i in range(0, len(netlist)):
				if funddate == netlist[i][0] and fundcode == netlist[i][1]:
					netlist[i][4] = totalasset

	result = GetCashAssetValue(I_startdate, I_enddate, I_fundcode)
	if result[0]:
		for funddate, fundcode, subname, cashasset, cashshare in result[1]:
			for i in range(0, len(netlist)):
				if funddate == netlist[i][0] and fundcode == netlist[i][1]:
					if cashasset != 0:
						netlist[i][5] = cashasset
					else:
						netlist[i][5] = cashshare * netlist[i][4]
	logger.debug('{0}'.format(netlist))
	return netlist

def OutputOplusFile(I_netlist, I_fundnamefile, I_outputpath):
	fundnamelist = dunhe_public.ReadExcel2List(I_fundnamefile)
	logger.debug('Fund name list: {0}'.format(fundnamelist))
	for fundcode, fundname in fundnamelist:
		fundnetinfolist = [['业务日期', '当前现金', '总资产', '净资产', '单位净值']]
		for funddate, netfundcode, netvalue, netasset, totalasset, cashasset in I_netlist:
			logger.debug('fundcode = {0}, netfundcode = {1}'.format(fundcode, netfundcode))
			if netfundcode == fundcode:
				fundnetinfolist.append([funddate, cashasset, totalasset, netasset, netvalue])
		if len(fundnetinfolist) > 1:
			filename = I_outputpath + fundname + '.xlsx'
			logger.debug('Fund[{0}] save to file[{1}] with data: {2}'.format(fundcode, filename, fundnetinfolist))
			dunhe_public.WriteData2Excel(fundnetinfolist, filename)
			logger.info('Save file {0} with {1} records.'.format(filename, len(fundnetinfolist) - 1))

logger = dunhe_public.SetLog('HisNetValueOutput')
STARTDATE = '20180101'
ENDDATE = '20190125'
FUNDCODELIST = ''
FUNDNAMEFILE = 'D:\\data\\Oplus产品信息.xls'
OUTPUTPATH = 'D:\\data\\hisnetvalue\\'

result = GetValue(STARTDATE, ENDDATE, FUNDCODELIST)
if len(result) > 0:
	OutputOplusFile(result, FUNDNAMEFILE, OUTPUTPATH)