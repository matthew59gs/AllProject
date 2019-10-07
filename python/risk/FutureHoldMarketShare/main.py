#!/usr/bin/env python
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import cx_Oracle
import pandas as pd
import pymysql

class market_hold_deal_share_calc:
    def __init__(self, logger):
        self.logger = logger
        self.union_sql = ' UNION ALL '
        self.wind_code_like_sql = ' AND regexp_like ( t.S_INFO_WINDCODE, \'[a-zA-Z]{1,2}[0-9]{3,4}.[A-Z]{3}\' )'
        self.wind_bond_sql = ' SELECT substr(t.S_INFO_WINDCODE, 1, instr(t.S_INFO_WINDCODE,\'.\') - 1) report_code, \
                                        t.TRADE_DT business_date, \
                                        t.S_DQ_OI holding, \
                                        t.S_DQ_VOLUME deal_amount, \
                                        t.S_DQ_AMOUNT deal_balance \
                                    FROM \
                                        CBondFuturesEODPrices t \
                                    WHERE 1 = 1 \
                                        AND t.TRADE_DT >= {0}  \
                                        AND t.TRADE_DT <= {1}  \
                                        AND t.S_DQ_OI > 0 '
        self.wind_fin_sql = 'SELECT substr(t.S_INFO_WINDCODE, 1, instr(t.S_INFO_WINDCODE, \'.\') - 1) report_code, \
                                        t.TRADE_DT business_date, \
                                        t.S_DQ_OI holding, \
                                        t.S_DQ_VOLUME deal_amount, \
                                        t.S_DQ_AMOUNT deal_balance \
                                    FROM \
                                        CINDEXFUTURESEODPRICES t  \
                                    WHERE 1 = 1 \
                                        AND t.TRADE_DT >= {0}  \
                                        AND t.TRADE_DT <= {1}  \
                                        AND t.S_DQ_OI > 0 '
        self.wind_comm_sql = 'SELECT substr(t.S_INFO_WINDCODE, 1, instr(t.S_INFO_WINDCODE, \'.\') - 1) report_code, \
                                        t.TRADE_DT business_date, \
                                        t.S_DQ_OI / 2 holding,  \
                                        t.S_DQ_VOLUME deal_amount, \
                                        t.S_DQ_AMOUNT deal_balance \
                                    FROM \
                                        CCOMMODITYFUTURESEODPRICES t  \
                                    WHERE 1 = 1 \
                                        AND t.TRADE_DT >= {0}  \
                                        AND t.TRADE_DT <= {1}  \
                                        AND t.S_DQ_OI > 0 '
        self.oplus_hold_sql = 'SELECT ' \
                              'a.business_date, ' \
                              'a.fund_id, ' \
                              'a.fund_name, ' \
                              'upper(a.report_code) report_code, ' \
                              'upper(tfk.future_kind_code) future_kind_code, ' \
                              'a.current_amount holding ' \
                              'FROM ' \
                              'tfundstock a, ' \
                              'tstockinfo_future tsf, ' \
                              'tfuturekind tfk ' \
                              'WHERE 1=1 ' \
                              'AND a.report_code = tsf.report_code ' \
                              'AND a.business_date = tsf.business_date ' \
                              'AND tsf.future_kind_id = tfk.future_kind_id ' \
                              'AND a.business_date >= {0} ' \
                              'AND a.business_date <= {1} '
        self.oplus_his_hold_sql = 'SELECT ' \
                              'a.business_date, ' \
                              'a.fund_id, ' \
                              'a.fund_name, ' \
                              'upper(a.report_code) report_code, ' \
                              'upper(tfk.future_kind_code) future_kind_code, ' \
                              'a.current_amount holding ' \
                              'FROM ' \
                              'thisfundstock a, ' \
                              'thisstockinfo_future tsf, ' \
                              'tfuturekind tfk ' \
                              'WHERE 1=1 ' \
                              'AND a.report_code = tsf.report_code ' \
                              'AND a.business_date = tsf.business_date ' \
                              'AND tsf.future_kind_id = tfk.future_kind_id ' \
                              'AND a.business_date >= {0} ' \
                              'AND a.business_date <= {1} '
        self.oplus_deal_sql = 'SELECT a.business_date, ' \
                              'a.fund_id,' \
                              'a.asset_id,' \
                              'a.report_code,' \
                              'tfk.future_kind_code,' \
                              'a.entrust_direction,' \
                              'a.deal_amount,' \
                              'a.deal_balance ' \
                              'FROM ' \
                              '(SELECT	trd.business_date, ' \
                              'trd.fund_id, ' \
                              'trd.asset_id,' \
                              'trd.report_code,' \
                              'max(trd.market_no) market_no, ' \
                              'trd.entrust_direction,' \
                              'sum( trd.deal_amount ) deal_amount,' \
                              'sum( trd.deal_amount * trd.deal_price ) deal_balance ' \
                              'FROM trealdeal trd ' \
                              'WHERE 1=1 ' \
                              'AND trd.business_date >= {0} ' \
                              'AND trd.business_date <= {1} ' \
                              'GROUP BY trd.fund_id, trd.asset_id, trd.report_code, trd.entrust_direction) a, ' \
                              'tstockinfo_future tsf, tfuturekind tfk ' \
                              'WHERE 1=1 ' \
                              'AND a.business_date = tsf.business_date ' \
                              'AND a.report_code = tsf.report_code ' \
                              'AND tsf.future_kind_id = tfk.future_kind_id '
        self.oplus_his_deal_sql = 'SELECT a.business_date, ' \
                              'a.fund_id,' \
                              'a.asset_id,' \
                              'a.report_code,' \
                              'tfk.future_kind_code,' \
                              'a.entrust_direction,' \
                              'a.deal_amount,' \
                              'a.deal_balance ' \
                              'FROM ' \
                              '(SELECT	trd.business_date, ' \
                              'trd.fund_id, ' \
                              'trd.asset_id,' \
                              'trd.report_code,' \
                              'max(trd.market_no) market_no, ' \
                              'trd.entrust_direction,' \
                              'sum( trd.deal_amount ) deal_amount,' \
                              'sum( trd.deal_amount * trd.deal_price ) deal_balance ' \
                              'FROM thisrealdeal trd ' \
                              'WHERE 1=1 ' \
                              'AND trd.business_date >= {0} ' \
                              'AND trd.business_date <= {1} ' \
                              'GROUP BY trd.fund_id, trd.asset_id, trd.report_code, trd.entrust_direction) a, ' \
                              'thisstockinfo_future tsf, tfuturekind tfk ' \
                              'WHERE 1=1 ' \
                              'AND a.business_date = tsf.business_date ' \
                              'AND a.report_code = tsf.report_code ' \
                              'AND tsf.future_kind_id = tfk.future_kind_id '

    # 获取万得历史行情数据，主要是持仓量，成交量，成交额
    # startdate:    格式yyyymmdd，数字，其实日期
    # enddate:	    格式yyyymmdd，数字，终止日期，值域[起始日期，终止日期]
    # exchange:     交易所序列，list，包含dunhe_public.Exchange的值
    # futurekind:   品种序列，list，包含str，品种代码都是大写
    # futurecode:   代码序列，list，包含str，代码都是大写
    # 返回Dataframe，格式为
    # report_cde[varchar], business_date[decimal], holding deal_amount[decimal], deal_balance[decimal]
    def get_market_data(self, startdate = 0, enddate = 0, exchange = None, futurekind = None, futurecode = None):
        if startdate == 0 or enddate == 0:
            self.logger.error('[get_market_data]start date or end date is 0!')
            return

        try:
            tns = cx_Oracle.makedsn('192.168.40.97', 1521, 'orcl')
            oracle_conn = cx_Oracle.connect('wind', 'wind@2019', tns)
        except Exception as e:
            self.logger.error("oracle connect fail: {0}".format(e))
            raise e
        else:
            cursor = oracle_conn.cursor()
            sql = ''
            try:
                if exchange is not None:
                    if dunhe_public.Exchange.CFFEX in exchange:
                        sql = sql + self.wind_bond_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                              self.union_sql + '\n' + \
                              self.wind_fin_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n'
                    if dunhe_public.Exchange.SHFE in exchange:
                        if sql != '':
                            sql = sql + self.union_sql + '\n'
                        sql = sql + self.wind_comm_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                              ' AND INSTR(t.S_INFO_WINDCODE, \'SHF\') > 0 ' + '\n'
                    if dunhe_public.Exchange.DCE in exchange:
                        if sql != '':
                            sql = sql + self.union_sql + '\n'
                        sql = sql + self.wind_comm_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                              ' AND INSTR(t.S_INFO_WINDCODE, \'DCE\') > 0 ' + '\n'
                    if dunhe_public.Exchange.CZCE in exchange:
                        if sql != '':
                            sql = sql + self.union_sql + '\n'
                        sql = sql + self.wind_comm_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                              ' AND INSTR(t.S_INFO_WINDCODE, \'CZC\') > 0 ' + '\n'
                    if dunhe_public.Exchange.INE in exchange:
                        if sql != '':
                            sql = sql + self.union_sql + '\n'
                        sql = sql + self.wind_comm_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                              ' AND INSTR(t.S_INFO_WINDCODE, \'INE\') > 0 ' + '\n'
                if futurekind is not None:
                    sql = sql + self.__make_sql_from_wincode(startdate, enddate, futurekind, sql)
                if futurecode is not None:
                    sql = sql + self.__make_sql_from_wincode(startdate, enddate, futurecode, sql)
                if exchange is None and futurekind is None and futurecode is None:
                    sql = self.wind_bond_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                          self.union_sql + '\n' + \
                          self.wind_fin_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n' + \
                          self.union_sql + '\n' + \
                          self.wind_comm_sql.format(startdate, enddate) + self.wind_code_like_sql + '\n'
                self.logger.debug('select sql: ' + sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                self.logger.info('Get {0} data from wind'.format(len(data)))

                df = pd.DataFrame(data)
                df.rename(columns={0:'report_code', 1:'business_date', 2:'holding', 3:'deal_amount',
                                   4:'deal_balance'}, inplace=True)
                df['business_date'] = df['business_date'].astype('int64')
                # DEBUG
                df.to_excel('get_market_data.xlsx')
                return df
            except Exception as e:
                self.logger.error("Sql execute error: {0}".format(e))
                raise e
            finally:
                cursor.close()
        oracle_conn.close()

    def __make_sql_from_wincode(self, startdate, enddate, codes, presql = ''):
        sql = ''
        for code in codes:
            code = code.upper()
            if presql != '':
                sql = sql + self.union_sql + '\n'
            sql = sql + self.wind_bond_sql.format(startdate, enddate) + '\n' + 'and INSTR(t.S_INFO_WINDCODE, \'{0}\') > 0 '.format(code) + '\n' + self.union_sql + '\n' + \
                      self.wind_fin_sql.format(startdate, enddate) + '\n' + 'and INSTR(t.S_INFO_WINDCODE, \'{0}\') > 0 '.format(code) + '\n' + self.union_sql + '\n' + \
                      self.wind_comm_sql.format(startdate, enddate) + '\n' + 'and INSTR(t.S_INFO_WINDCODE, \'{0}\') > 0 '.format(code) + '\n'
        return sql

    # 获取Oplus持仓数据，维度为产品
    # startdate:    格式yyyymmdd，数字，其实日期
    # enddate:	    格式yyyymmdd，数字，终止日期，值域[起始日期，终止日期]
    # exchange:     交易所序列，list，包含dunhe_public.Exchange的值
    # futurekind:   品种序列，list，包含str，品种代码都是大写
    # futurecode:   代码序列，list，包含str，代码都是大写
    # fundlist:     产品序号序列，list，包含int
    # 返回Dataframe，格式为
    # business_date[decimal], fund_id[decimal], fund_name[varchar], report_cde[varchar], future_kind_code[varchar], holding[decimal]
    def get_oplus_holding_data(self, startdate = 0, enddate = 0, exchange = None, futurekind = None, futurecode = None, fundlist = None):
        df = self.__get_oplus_data(mode='hold', startdate=startdate, enddate=enddate, exchange=exchange,
                                     futurekind=futurekind, futurecode=futurecode, fundlist=fundlist)
        df.rename(columns={0:'business_date', 1:'fund_id', 2:'fund_name', 3:'report_code', 4:'future_kind_code',
                           5:'holding'},
                  inplace=True)
        # DEBUG
        df.to_excel('get_oplus_holding_data.xlsx')
        return df

    # 获取Oplus成交数据，维度为产品
    # startdate:    格式yyyymmdd，数字，其实日期
    # enddate:	    格式yyyymmdd，数字，终止日期，值域[起始日期，终止日期]
    # exchange:     交易所序列，list，包含dunhe_public.Exchange的值
    # futurekind:   品种序列，list，包含str，品种代码都是大写
    # futurecode:   代码序列，list，包含str，代码都是大写
    # fundlist:     产品序号序列，list，包含int
    # 返回Dataframe，格式为
    # business_date[decimal], fund_id[decimal], asset_id[decimal], report_cde[varchar], future_kind_code[varchar],
    # entrust_direction[varchar], deal_amount[decimal], deal_balance[decimal]
    def get_oplus_dealing_data(self, startdate = 0, enddate = 0, exchange = None, futurekind = None, futurecode = None, fundlist = None):
        df = self.__get_oplus_data(mode='deal', startdate=startdate, enddate=enddate, exchange=exchange,
                                     futurekind=futurekind, futurecode=futurecode, fundlist=fundlist)
        df.rename(columns={0:'business_date', 1:'fund_id', 2:'asset_id', 3:'report_code', 4:'future_kind_code',
                           5:'entrust_direction', 6:'deal_amount', 7:'deal_balance'},
                  inplace=True)
        # DEBUG
        df.to_excel('get_oplus_dealing_data.xlsx')
        return df

    def __get_oplus_data(self, mode='', startdate = 0, enddate = 0, exchange = None, futurekind = None, futurecode = None, fundlist = None):
        if mode == '':
            return
        if startdate == 0 or enddate == 0:
            self.logger.error('[get_oplus_data]start date or end date is 0!')
            return

        if mode == 'deal':
            base_sql = self.oplus_deal_sql
        if mode == 'hold':
            base_sql = self.oplus_hold_sql
        sql = ''
        if fundlist is not None:
            sql = base_sql.format(startdate, enddate) + ' AND a.fund_id IN (' + ','.join(
                map(lambda x: str(x), fundlist)) + ') ' + '\n'
            if exchange is not None:
                sql = sql + ' AND a.market_no IN (\'' + '\',\''.join(exchange) + '\') ' + '\n'
            if futurekind is not None:
                sql = sql + 'and upper(tfk.future_kind_code) in (\'' + '\',\''.join(futurekind) + '\') ' + '\n'
            if futurecode is not None:
                sql = sql + 'and upper(a.report_code) in (\'' + '\',\''.join(futurecode) + '\') ' + '\n'
        else:
            sql = base_sql.format(startdate, enddate)
            if exchange is not None:
                sql = sql + ' AND a.market_no IN (\'' + '\',\''.join(exchange) + '\') ' + '\n'
            if futurekind is not None:
                sql = sql + ' and upper(tfk.future_kind_code) in (\'' + '\',\''.join(futurekind) + '\') ' + '\n'
            if futurecode is not None:
                sql = sql + ' and upper(a.report_code) in (\'' + '\',\''.join(futurecode) + '\') ' + '\n'

        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='oplus', password='oplus', db='oplus_p', charset='utf8')
        except Exception as e:
            if logger:
                logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                logger.debug('select sql: ' + sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                df = pd.DataFrame(list(data))
                logger.info('Get {0} holding data from oplus'.format(len(data)))
                return df
            except Exception as e:
                self.logger.error('Sql execute error: {0}'.format(e))
                raise e
            finally:
                cursor.close()
                conn.close()

    def get_holding_share(self, startdate = 0, enddate = 0, exchange = None, futurekind = None, futurecode = None, fundlist = None):
        if startdate == 0 or enddate == 0:
            self.logger.error('[get_holding_share]start date or end date is 0!')
            return

        df_wind = self.get_market_data(startdate=startdate, enddate=enddate, exchange=exchange, futurekind=futurekind,
                                       futurecode=futurecode)
        #df_wind = pd.DataFrame(pd.read_excel('get_market_data.xlsx'))
        df_oplus_hold = self.get_oplus_holding_data(startdate=startdate, enddate=enddate, exchange=exchange,
                                                    futurekind=futurekind, futurecode=futurecode, fundlist=fundlist)
        #df_oplus_hold = pd.DataFrame(pd.read_excel('get_oplus_holding_data.xlsx'))
        df_merge = pd.merge(df_oplus_hold, df_wind, on=['business_date', 'report_code'], how=['left'])
        df_merge.rename(columns={'holding': 'market_hold'}, inplace=True)
        df_merge['share'] = round(df_merge['holding'] / df['market_hold'] * 100, 2)
        return df_merge

logger = dunhe_public.SetLog('FutureHoldMarketShare')
calc = market_hold_deal_share_calc(logger)
df = calc.get_holding_share(startdate=20190601, enddate=20190627)
print(df)
