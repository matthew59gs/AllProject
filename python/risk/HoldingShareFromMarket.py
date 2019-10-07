#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 从wind库读取当日市场数据，形成临时表，进入market_holding表
# 从Oplus读取当日持仓数据，形成临时表，进入company_holding表
# tradesplit库做表汇总分析，形成Excel
# 需要下载cx_oracle

import pymysql
import datetime
import cx_Oracle
import os
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

# Wind库读取数据，写入tradesplit库的market_holding表


def GetWindData():
    wind_insert_sql = ''
    try:
        tns = cx_Oracle.makedsn('192.168.40.97', 1521, 'orcl')
        oracle_conn = cx_Oracle.connect('wind', 'wind', tns)
    except Exception as e:
        logger.error("oracle connect fail: {0}".format(e))
        raise e
    else:
        cursor = oracle_conn.cursor()
        try:
            sql = 'SELECT \
				t.S_INFO_WINDCODE, \
				t.TRADE_DT, \
				t.S_DQ_OI / 2 S_DQ_OI  \
			FROM \
				CCOMMODITYFUTURESEODPRICES t  \
			WHERE 1 = 1 \
				AND t.TRADE_DT >= ' + HQ_BEGIN_DATE + '  \
				AND t.TRADE_DT <=' + HQ_END_DATE + '  \
				AND t.S_DQ_OI > 0  \
				AND regexp_like ( t.S_INFO_WINDCODE, \'[a-zA-Z]{1,2}[0-9]{3,4}.[A-Z]{3}\' ) UNION ALL \
			SELECT \
				ti.S_INFO_WINDCODE, \
				ti.TRADE_DT, \
				ti.S_DQ_OI  \
			FROM \
				CINDEXFUTURESEODPRICES ti  \
			WHERE 1 = 1 \
				AND ti.TRADE_DT >= ' + HQ_BEGIN_DATE + '  \
				AND ti.TRADE_DT <=' + HQ_END_DATE + '  \
				AND ti.S_DQ_OI > 0  \
				AND regexp_like ( ti.S_INFO_WINDCODE, \'[a-zA-Z]{1,2}[0-9]{3,4}.[A-Z]{3}\' ) UNION ALL \
			SELECT \
				tb.S_INFO_WINDCODE, \
				tb.TRADE_DT, \
				tb.S_DQ_OI  \
			FROM \
				CBondFuturesEODPrices tb \
			WHERE 1 = 1 \
				AND tb.TRADE_DT >= ' + HQ_BEGIN_DATE + '  \
				AND tb.TRADE_DT >= ' + HQ_END_DATE + '  \
				AND tb.S_DQ_OI > 0  \
				AND regexp_like ( tb.S_INFO_WINDCODE, \'[a-zA-Z]{1,2}[0-9]{3,4}.[A-Z]{3}\' )'
            logger.debug('select sql: ' + sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            logger.info('Get {0} data from wind'.format(len(data)))
            for windcode, tradedate, marketholding in data:
                wind_insert_sql += '(\'{0}\', \'{1}\', {2}),'.format(
                    windcode, tradedate, marketholding)
            if (len(data) > 0):
                wind_insert_sql = 'INSERT INTO market_holding(windcode, tradedate, marketholding) VALUES ' + \
                    wind_insert_sql
                wind_insert_sql = wind_insert_sql[
                    :len(wind_insert_sql) - 1] + ';'
        except Exception as e:
            logger.error("Sql execute error: {0}".format(e))
            raise e
        finally:
            cursor.close()
            oracle_conn.close()
    return wind_insert_sql

# Oplus库读取数据，写入tradesplit库的


def GetOplusData():
    oplus_insert_sql = ''
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
				t.business_date, \
				t.report_code, \
				t.position_type, \
				sum( t.current_amount ) current_amount  \
			FROM \
				tfundstock t  \
			WHERE 1 = 1 \
				AND t.business_date >= {0}  \
				AND t.business_date <= {1}  \
				AND t.market_no IN (\'9\')  \
				AND t.position_type in (\'1\',\'2\') \
				AND t.current_amount > 0  \
			GROUP BY \
				t.business_date, \
				t.position_type, \
				t.report_code;'.format(HQ_BEGIN_DATE, HQ_END_DATE)
            logger.debug('select sql: ' + sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            logger.info('Get {0} data from oplus'.format(len(data)))
            for business_date, report_code, position_type, current_amount in data:
                oplus_insert_sql += '(\'{0}\', \'{1}\', \'{2}\', {3}),'.format(
                    business_date, report_code, position_type, current_amount)
            if (len(data) > 0):
                oplus_insert_sql = 'INSERT INTO company_holding(business_date, report_code, position_type, current_amount) VALUES ' + \
                    oplus_insert_sql
                oplus_insert_sql = oplus_insert_sql[
                    :len(oplus_insert_sql) - 1] + ';'
        except Exception as e:
            logger.error("Sql execute error: {0}".format(e))
            raise e
        finally:
            cursor.close()
            mysql_conn.close()
    return oplus_insert_sql

# wind进入market_holding表，Oplus进入company_holding表
# 表数据整理后写入Excel


def MergeDataIntoExcel(wind_insert_sql, oplus_insert_sql, path):
    EXCEL_NAME = '期货持仓占比概况'
    SUFFIX_NAME = '.xlsx'
    save_file = ''
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
            if wind_insert_sql != '':
                try:
                    sql = 'DELETE FROM market_holding WHERE tradedate >= \'{0}\' AND tradedate <= \'{1}\';'.format(
                        HQ_BEGIN_DATE, HQ_END_DATE)
                    logger.debug('delete sql: ' + sql)
                    cursor.execute(sql)
                    mysql_conn.commit()
                    logger.debug("insert sql: " + wind_insert_sql)
                    cursor.execute(wind_insert_sql)
                    mysql_conn.commit()
                except Exception as e:
                    logger.error("Sql execute error: {0}".format(e))
            if oplus_insert_sql != '':
                try:
                    sql = 'DELETE FROM company_holding WHERE business_date >= \'{0}\' AND business_date <= \'{1}\';'.format(
                        HQ_BEGIN_DATE, HQ_END_DATE)
                    logger.debug('delete sql: ' + sql)
                    cursor.execute(sql)
                    mysql_conn.commit()
                    logger.debug("insert sql: " + oplus_insert_sql)
                    cursor.execute(oplus_insert_sql)
                    mysql_conn.commit()
                    sql = 'UPDATE company_holding set future_code = LEFT ( report_code, 2 ) WHERE LEFT ( report_code, 2 ) REGEXP \'[a-zA-Z]{2}\';'
                    cursor.execute(sql)
                    mysql_conn.commit()
                    sql = 'UPDATE company_holding set future_code = LEFT ( report_code, 1 ) WHERE LEFT ( report_code, 2 ) REGEXP \'[a-zA-Z]{1}\' AND future_code is null;'
                    cursor.execute(sql)
                    mysql_conn.commit()
                except Exception as e:
                    logger.error("Sql execute error: {0}".format(e))

            # 数据整理后进入临时表
            # 合约临时表
            '''
            sql = 'CREATE TEMPORARY TABLE holding_detail( \
					`business_date` VARCHAR(20), \
					`position_type` VARCHAR(20), \
					`report_code` VARCHAR(20), \
					`future_code` VARCHAR(20), \
					`current_amount` DOUBLE(20, 4), \
					`marketholding` DOUBLE(20, 4), \
					`share` VARCHAR(20) \
					);'
            logger.debug('creat temp table sql: ' + sql)
            cursor.execute(sql)
            mysql_conn.commit()
            '''
            sql = 'DELETE FROM holding_detail WHERE tradedate >= \'{0}\' AND tradedate <= \'{1}\';'.format(
                        HQ_BEGIN_DATE, HQ_END_DATE)
            logger.debug('delete sql: ' + sql)
            cursor.execute(sql)
            mysql_conn.commit()
            sql = 'INSERT INTO holding_detail(business_date, position_type, report_code, future_code, current_amount, marketholding, `share`) \
				SELECT \
					t.business_date, \
					t.position_type, \
					t.report_code, \
					t.future_code, \
					t.current_amount, \
					m.marketholding, \
					concat( round( t.current_amount / m.marketholding * 100, 2 ), \'%\' ) `share` \
				FROM \
					( \
				SELECT \
					tm.tradedate, \
					tm.windcode, \
					tm.marketholding, \
				CASE \
					WHEN LEFT ( tm.windcode, 2 ) REGEXP \'[a-zA-Z]{2}\' THEN \
					UPPER(LEFT ( tm.windcode, 2 ) ) \
					WHEN LEFT ( tm.windcode, 1 ) REGEXP \'[a-zA-Z]{1}\' THEN \
					UPPER(LEFT ( tm.windcode, 1 ) ) ELSE \'\'  \
					END futurecode  \
				FROM \
					market_holding tm  \
				WHERE 1 = 1 \
					AND tm.tradedate >= \'' + HQ_BEGIN_DATE + '\'  \
					AND tm.tradedate <= \'' + HQ_END_DATE + '\'  \
					) m \
					RIGHT JOIN ( \
				SELECT \
					tc.business_date, \
					tc.position_type, \
					tc.report_code, \
					tc.future_code, \
					tc.current_amount  \
				FROM \
					company_holding tc  \
				WHERE 1 = 1 \
					AND tc.business_date >= \'' + HQ_BEGIN_DATE + '\'  \
					AND tc.business_date <= \'' + HQ_END_DATE + '\'  \
					) t ON SUBSTRING_INDEX(m.windcode, \'.\', 1) = UPPER(t.report_code) \
					AND t.business_date = m.tradedate  \
				ORDER BY \
					t.position_type, \
					t.report_code;'
            logger.debug('insert sql: ' + sql)
            cursor.execute(sql)
            mysql_conn.commit()
            # 品种临时表
            '''
            sql = 'CREATE TEMPORARY TABLE holding_gathering( \
					`business_date` VARCHAR(20), \
					`position_type` VARCHAR(20), \
					`future_code` VARCHAR(20), \
					`current_amount` DOUBLE(20, 4), \
					`marketholding` DOUBLE(20, 4), \
					`share` VARCHAR(20) \
					);'
            logger.debug('creat temp table sql: ' + sql)
            cursor.execute(sql)
            mysql_conn.commit()
            '''
            sql = 'DELETE FROM holding_gathering WHERE tradedate >= \'{0}\' AND tradedate <= \'{1}\';'.format(
                        HQ_BEGIN_DATE, HQ_END_DATE)
            logger.debug('delete sql: ' + sql)
            cursor.execute(sql)
            mysql_conn.commit()
            sql = 'INSERT INTO holding_gathering(business_date, future_code, position_type, current_amount, marketholding, `share`) \
				SELECT \
				t.business_date, \
				t.future_code, \
				t.position_type, \
				t.current_amount, \
				m.marketholding, \
				concat( round( t.current_amount / m.marketholding * 100, 2 ), \'%\' ) `share`  \
			FROM \
				( \
			SELECT \
				tmf.tradedate date, \
				UPPER( tmf.futurecode ) futurecode, \
				sum( tmf.marketholding ) marketholding  \
			FROM \
				( \
			SELECT \
				tm.tradedate, \
				tm.windcode, \
				tm.marketholding, \
			CASE \
				WHEN LEFT ( tm.windcode, 2 ) REGEXP \'[a-zA-Z]{2}\' THEN \
				LEFT ( tm.windcode, 2 )  \
				WHEN LEFT ( tm.windcode, 1 ) REGEXP \'[a-zA-Z]{1}\' THEN \
				LEFT ( tm.windcode, 1 ) ELSE \'\'  \
				END futurecode  \
			FROM \
				market_holding tm  \
			WHERE 1 = 1 \
				AND tm.tradedate >= \'' + HQ_BEGIN_DATE + '\'  \
				AND tm.tradedate <= \'' + HQ_END_DATE + '\'  \
				) tmf  \
			GROUP BY \
				tmf.tradedate, \
				tmf.futurecode  \
				) m RIGHT JOIN  \
				( \
			SELECT \
				tc.business_date, \
				tc.future_code, \
				tc.position_type, \
				sum( tc.current_amount ) current_amount  \
			FROM \
				company_holding tc  \
			WHERE 1 = 1 \
				AND tc.business_date >= \'' + HQ_BEGIN_DATE + '\'  \
				AND tc.business_date <= \'' + HQ_END_DATE + '\'  \
			GROUP BY \
				tc.business_date, \
				tc.future_code, \
			tc.position_type	 \
				) t \
				ON m.futurecode = t.future_code and m.date = t.business_date ;'
            logger.debug('insert sql: ' + sql)
            cursor.execute(sql)
            mysql_conn.commit()
            # 临时表联合查询
            sql = 'SELECT \
				d.business_date \'日期\', \
				CASE  \
				WHEN d.position_type = \'1\' THEN \
				\'多\'  \
				WHEN d.position_type = \'2\' THEN \
				\'空\' \
				ELSE d.position_type  \
				END \'方向\', \
				d.future_code \'品种\', \
				g.current_amount \'公司品种持仓量\', \
				g.marketholding \'市场品种单边持仓量\', \
				g.`share` \'占比\', \
				d.report_code \'合约\', \
				d.current_amount \'合约公司持仓量\', \
				d.marketholding \'合约市场单边持仓量\', \
				d.`share` \'占比\' \
			FROM \
				holding_detail d \
				LEFT JOIN holding_gathering g ON d.position_type = g.position_type  \
				AND d.future_code = g.future_code  AND d.business_date = g.business_date \
			ORDER BY \
				d.business_date, \
				d.position_type, \
				d.future_code, \
				d.report_code;'
            logger.debug('selet sql: ' + sql)
            cursor.execute(sql)
            # 标题加到数据中
            data = []
            title = []
            for field_desc in cursor.description:
                title.append(field_desc[0])
            data.append(tuple(title))
            for row in cursor.fetchall():
                data.append(row)
            logger.debug('data is: {0}'.format(data))

            # 有明细数据就有汇总数据，写入Excel
            save_file = os.path.join(
                path, HQ_BEGIN_DATE + EXCEL_NAME + SUFFIX_NAME)
            dunhe_public.WriteData2Excel(data, save_file)
        except Exception as e:
            logger.error("Sql execute error: {0}".format(e))
            raise e
        finally:
            cursor.close()
            mysql_conn.close()
    return save_file


# 主变量
# 日志
logger = dunhe_public.SetLog('HoldingShareFromMarket')
# 读取哪天的行情
#HQ_DATE_OPLUS = datetime.datetime.now().strftime("%Y%m%d")
#HQ_DATE_WIND = datetime.datetime.now().strftime("%Y%m%d")
#HQ_DATE_OPLUS = '20181029'
#HQ_DATE_WIND = '20181029'
HQ_BEGIN_DATE = '20180101'
HQ_END_DATE = '20190217'
# 文件保存位置
SAVE_PATH = "G:\\data\\risk"
ESCAPE_SENDING = 1  # 0-发送，1-不发送
RECIEVE_LIST = ['gaos@dunhefund.com',
                'tanghj@dunhefund.com', 'panhm@dunhefund.com']
# RECIEVE_LIST=['gaos@dunhefund.com']

file = MergeDataIntoExcel(GetWindData(), GetOplusData(), SAVE_PATH)
if not ESCAPE_SENDING and file != '':
    dunhe_public.SendingMailFromIT(RECIEVE_LIST, '', '', file)
