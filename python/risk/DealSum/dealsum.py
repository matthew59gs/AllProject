# -*- coding:utf-8 -*-
import datetime
import pymysql
import pandas as pd
import os

DEBUG = 0
DIRECTION_REPLACE_DICT_TO_NUM = {'买入开仓': 32, '卖出平仓': 33, '卖出开仓': 34, '买入平仓': 35}
DIRECTION_REPLACE_DICT_TO_STR = {32: '买入开仓', 33: '卖出平仓', 34: '卖出开仓', 35: '买入平仓'}


class DealSum:
    def __init__(self, logger):
        self.logger = logger

    def calc_deal(self, date_list=[], contract_list=[], product_list=[], entrust_direction=[], path=''):
        if path == '':
            return

        sql = 'SELECT t.business_date, t.deal_time, t.report_code, t.fund_name, t.deal_amount, t.deal_price, t.entrust_direction from trealdeal t WHERE 1=1 '
        if len(date_list) > 0:
            sql_date = ' AND t.business_date >= ' + date_list[0]
            if len(date_list) > 1:
                sql_date = sql_date + ' AND t.business_date <= ' + date_list[1]
            sql = sql + sql_date
        if len(contract_list) > 0:
            sql_contract = ' AND upper(t.report_code) in (\'{0}\')'.format('\',\''.join(contract_list))
            sql = sql + sql_contract
        if len(product_list) > 0:
            self.logger.debug('product_list = {0}'.format(product_list))
            sql_product = ' AND t.fund_name in (\'{0}\')'.format('\',\''.join(product_list))
            sql = sql + sql_product
        if len(entrust_direction) > 0:
            rep_entrust_direction = [str(DIRECTION_REPLACE_DICT_TO_NUM[x]) if x in DIRECTION_REPLACE_DICT_TO_NUM else x for x in entrust_direction]
            sql_entrust_direction = ' AND t.entrust_direction in ({0})'.format(','.join(rep_entrust_direction))
            sql = sql + sql_entrust_direction
        sql = sql + ' ORDER BY t.business_date, t.deal_time, t.report_code, t.fund_name'
        if not DEBUG:
            try:
                connection = pymysql.connect(host='192.168.40.202', port=3306,
                                             user='oplus', password='oplus',
                                             db='oplus_p',
                                             charset='utf8')
            except Exception as e:
                self.logger.error("Sever connect fail: {0}".format(e))
            else:
                self.logger.debug('select sql:' + sql)
                df = pd.read_sql(sql, connection)
                df.to_excel(os.path.join(path, '1.xlsx'))
                self.logger.debug('ori deal data: {0}'.format(df))
        else:
            df = pd.read_excel(os.path.join(path, '1.xlsx'))

        sort_num = 0
        df['deal_balance'] = df['deal_amount'] * df['deal_price']
        df['sort_num'] = sort_num
        col_num = 8
        stand_serial = df.iloc[0]
        self.logger.debug('stand row business_date[{0}], deal_time[{1}], report_code[{2}], fund_name[{3}]'.format(
                stand_serial['business_date'], stand_serial['deal_time'],
                stand_serial['report_code'], stand_serial['fund_name']
            ))
        for row_num in range(df.shape[0]):
            row = df.iloc[row_num]
            if row['business_date'] != stand_serial['business_date'] or \
                    row['report_code'] != stand_serial['report_code'] or \
                    row['fund_name'] != stand_serial['fund_name'] or \
                    abs(int(row['deal_time']) - int(stand_serial['deal_time'])) > 500:
                sort_num = sort_num + 1
                stand_serial = row
                self.logger.debug('new sort_num[{0}]'.format(sort_num))
                self.logger.debug(
                    'stand row business_date[{0}], deal_time[{1}], report_code[{2}], fund_name[{3}]'.format(
                        stand_serial['business_date'], stand_serial['deal_time'],
                        stand_serial['report_code'], stand_serial['fund_name']))
            df.iloc[row_num, col_num] = sort_num
        self.logger.debug('sort deal data: {0}'.format(df))
        if DEBUG:
            df.to_excel(os.path.join(path, '2.xlsx'))

        group = df.groupby(by='sort_num').agg({'business_date': max, 'deal_time': ['min', 'max'], 'report_code': max,
                                              'fund_name': max, 'deal_amount': sum, 'deal_balance': sum,
                                               'entrust_direction': max})
        self.logger.debug('group result: {0}'.format(group))
        if DEBUG:
            group.to_excel(os.path.join(path, '3.xlsx'))

        group.reset_index()
        grouped_df = pd.DataFrame(group.copy())
        grouped_df.reset_index()
        grouped_df.columns = ['business_date', 'deal_time_min', 'deal_time_max', 'contract', 'fund_name',
                              'deal_amount', 'deal_balance', 'entrust_direction']
        grouped_df['avg_price'] = grouped_df['deal_balance'] / grouped_df['deal_amount']
#        grouped_df['entrust_direction'] = df['entrust_direction'].apply(lambda x: '买入开仓' if x == 32 else(
#            '卖出平仓' if x == 33 else ('卖出开仓' if x == 34 else '买入平仓')))
        grouped_df['entrust_direction'] = grouped_df['entrust_direction'].map(DIRECTION_REPLACE_DICT_TO_STR)
        self.logger.info('grouped data: {0}'.format(grouped_df))
        grouped_df.to_excel(os.path.join(path, 'result.xlsx'))