# -*- coding:utf-8 -*-
# 三个需要手工处理的地方
# 1、保证金比例，生成了excel之后，让风控把提保幅度加上就好，这里需要手工生成一个excel
# 2、期货账户资金，从oplus的期货查询界面直接查询，然后手工导入，程序识别导入
# 3、生成了excel之后，计算

import os
import pymysql
import sys
import datetime
import pandas as pd
import numpy as np
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public


class RaiseDepositRatio:
    def __init__(self, logger, base_date):
        self.logger = logger
        self.base_date = base_date
        self.is_data_clear = False

    def get_current_ratio(self, excel_out_path):
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306, user='oplus', password='oplus',
                                   db='oplus_p', charset='utf8')
        except Exception as e:
            self.logger.error("Sever connect fail: {0}".format(e))
        else:
            try:
                sql = 'select ta.capital_account_name, ta.broker_name, b.invest_type, b.future_kind_code, ' \
                      'b.report_code, b.margin_ratio from tcapitalaccount ta,' \
                      '(SELECT tdf.capital_account_id, tdf.invest_type, tfk.future_kind_code, ' \
                      'min(tdf.report_code) report_code, tdf.margin_ratio ' \
                      'from tdepositset_future tdf, tfuturekind tfk,' \
                      '(SELECT tsf.future_kind_id, tsf.report_code ' \
                      'from tstockinfo_future tsf WHERE 1=1 and tsf.business_date = {0})a ' \
                      'WHERE 1=1 and a.report_code = tdf.report_code ' \
                      'and a.future_kind_id = tfk.future_kind_id and tdf.margin_ratio >0 ' \
                      'GROUP BY tdf.capital_account_id, tdf.invest_type, tfk.future_kind_code, tdf.margin_ratio)b ' \
                      'where b.capital_account_id = ta.capital_account_id'.format(self.base_date)
                self.logger.debug('Select sql: ' + sql)
                df = pd.DataFrame(pd.read_sql_query(sql, conn))
                filename = os.path.join(excel_out_path, '{0}当前保证金比例.xlsx'.format(self.base_date))
                df.to_excel(filename)
                self.logger.info('Output excel file [{0}] with current ratio'.format(filename))
            finally:
                conn.close()

    # 数据库里面的新保证金比例清空
    def clear_ratio_change(self):
        if self.is_data_clear:
            return

        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306, user='oplus', password='oplus',
                                   db='oplus_p', charset='utf8')
        except Exception as e:
            self.logger.error("Sever connect fail: {0}".format(e))
        else:
            cursor = conn.cursor()
            try:
                sql = 'delete from OUTER_tdepositset_future'
                self.logger.debug('Delete sql: ' + sql)
                cursor.execute(sql)
                conn.commit()
                sql = 'insert into OUTER_tdepositset_future(manage_filename, capital_account_id, market_no, report_code, invest_type, ' \
                      'stockholder_id, margin_ratio, short_margin_ratio, future_kind_code) ' \
                      'SELECT tdf.manage_filename, tdf.capital_account_id, tdf.market_no, tdf.report_code, tdf.invest_type,' \
                      'tdf.stockholder_id, tdf.margin_ratio, tdf.short_margin_ratio, tfk.future_kind_code ' \
                      'FROM tdepositset_future tdf, tfuturekind tfk,' \
                      '( SELECT tsf.future_kind_id, tsf.report_code FROM tstockinfo_future tsf WHERE 1 = 1 AND tsf.business_date = {0} ) a ' \
                      'WHERE 1 = 1 AND a.report_code = tdf.report_code AND a.future_kind_id = tfk.future_kind_id AND tdf.margin_ratio > 0'.format(self.base_date)
                self.logger.debug('Insert sql: ' + sql)
                cursor.execute(sql)
                conn.commit()
            finally:
                cursor.close()
                conn.close()
        self.is_data_clear = True

    def import_new_ratio_with_ratio_share(self, execl_in_path):
        df = pd.DataFrame(pd.read_excel(execl_in_path))
        raise_data = df['raise'].groupby(df['future_kind_code'])
        self.logger.debug('Future code raise ratio:\n{0}'.format(raise_data.min()))

        self.clear_ratio_change()

        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306, user='oplus', password='oplus',
                                   db='oplus_p', charset='utf8')
        except Exception as e:
            self.logger.error("Sever connect fail: {0}".format(e))
        else:
            cursor = conn.cursor()
            try:
                for name, group in raise_data:
                    value = group.min()
                    if not np.isnan(value):
                        sql = 'UPDATE OUTER_tdepositset_future t set ' \
                              't.new_margin_ratio = round(t.margin_ratio + {0}, 2) ' \
                              'WHERE t.future_kind_code = \'{1}\''.format(value, name)
                        self.logger.debug('Update sql: ' + sql)
                        cursor.execute(sql)
                        conn.commit()
                sql = 'UPDATE OUTER_tdepositset_future set new_margin_ratio = margin_ratio WHERE new_margin_ratio is null;'
                self.logger.debug('Update sql: ' + sql)
                cursor.execute(sql)
                conn.commit()
            finally:
                cursor.close()
                conn.close()

    def import_new_ratio_with_fix_ratio(self, execl_in_path):
        df = pd.DataFrame(pd.read_excel(execl_in_path))
        self.logger.debug('Future code ratio:\n{0}'.format(df))

        self.clear_ratio_change()

        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306, user='oplus', password='oplus',
                                   db='oplus_p', charset='utf8')
        except Exception as e:
            self.logger.error("Sever connect fail: {0}".format(e))
        else:
            cursor = conn.cursor()
            try:
                for index, row in df.iterrows():
                    if not np.isnan(row['market_no']):
                        sql = 'UPDATE OUTER_tdepositset_future t set t.new_margin_ratio = {0} ' \
                              'where t.market_no = {1} ' \
                              'AND t.margin_ratio < {0}'.format(row['fix_ratio'], row['market_no'])
                    else:
                        sql = 'UPDATE OUTER_tdepositset_future t set t.new_margin_ratio = {0} ' \
                              'WHERE t.future_kind_code = \'{1}\' ' \
                              'AND t.margin_ratio < {0}'.format(row['fix_ratio'], row['future_kind_code'])
                    self.logger.debug('Update sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()

                sql = 'UPDATE OUTER_tdepositset_future set new_margin_ratio = margin_ratio ' \
                      'WHERE new_margin_ratio is null;'
                self.logger.debug('Update sql: ' + sql)
                cursor.execute(sql)
                conn.commit()
            finally:
                cursor.close()
                conn.close()

    def generate_account_raise_table(self, capital_data_in_path, excel_out_path, only_select=False):
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306, user='oplus', password='oplus',
                                   db='oplus_p', charset='utf8')
        except Exception as e:
            self.logger.error("Sever connect fail: {0}".format(e))
        else:
            cursor = conn.cursor()
            try:
                if not only_select:
                    # 1 生成持仓占用保证金变动和盈亏变动数据
                    sql = 'DELETE FROM OUTER_fund_margin_detail'
                    self.logger.debug('Delete sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
                    sql = 'INSERT into OUTER_fund_margin_detail (business_date, fund_id, asset_id, report_code, ' \
                          'current_amount, margin_ratio, new_margin_ratio, price, margin, new_margin, ' \
                          'three_margin, three_profit, five_margin, five_profit, eight_margin, eight_profit) ' \
                          'SELECT tus.business_date, tus.fund_id, tus.asset_id, tus.report_code, tus.current_amount, ' \
                          'tdf.margin_ratio, tdf.new_margin_ratio, tsf.last_price, ' \
                          'tus.current_amount*tdf.margin_ratio*tfk.multiple*tsf.last_price margin, ' \
                          'tus.current_amount*tdf.new_margin_ratio*tfk.multiple*tsf.last_price new_margin, ' \
                          'tus.current_amount*tdf.new_margin_ratio*tfk.multiple*tsf.last_price*(case tus.position_type when \'1\' then 0.97 else 1.03 end) three_margin, ' \
                          'tus.current_amount*tfk.multiple*0.03*tsf.last_price*(-1) three_profit, ' \
                          'tus.current_amount*tdf.new_margin_ratio*tfk.multiple*tsf.last_price*(case tus.position_type when \'1\' then 0.95 else 1.05 end) five_margin, ' \
                          'tus.current_amount*tfk.multiple*0.05*tsf.last_price*(-1) five_profit, ' \
                          'tus.current_amount*tdf.new_margin_ratio*tfk.multiple*tsf.last_price*(case tus.position_type when \'1\' then 0.92 else 1.08 end) eight_margin, ' \
                          'tus.current_amount*tfk.multiple*0.08*tsf.last_price*(-1) eight_profit ' \
                          'FROM tunitstock tus, tfuturekind tfk, tstockinfo_future tsf, ' \
                          'OUTER_tdepositset_future tdf, tassetcapital tac ' \
                          'WHERE 1=1 and tus.business_date = {0} and ' \
                          'tus.market_no in (\'3\', \'4\', \'7\', \'9\', \'34\') and tus.current_amount > 0 ' \
                          'and tsf.business_date = tus.business_date and tsf.report_code = tus.report_code ' \
                          'and tfk.future_kind_id = tsf.future_kind_id and tus.report_code = tdf.report_code ' \
                          'and tus.invest_type = tdf.invest_type and tdf.capital_account_id = tac.capital_account_id ' \
                          'and tac.asset_id = tus.asset_id'.format(self.base_date)
                    self.logger.debug('Insert sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()

                    # 2 导入资金数据
                    sql = 'delete from OUTER_imp_future_asset'
                    self.logger.debug('Delete sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
                    df = pd.DataFrame(pd.read_excel(capital_data_in_path))
                    df.rename(columns={'日期': 'business_date', '产品名称': 'fundname', '单元名称': 'assetname',
                                       '当前权益': 'asset', '保证金占用(不含挂单)': 'holding'}, inplace=True)
                    for index, row in df.iterrows():
                        sql = 'insert into OUTER_imp_future_asset(business_date, fundname, assetname, asset, holding) ' \
                              'values({0}, \'{1}\', \'{2}\', {3}, {4})'.format(row['business_date'].replace('-', ''),
                                                                               row['fundname'], row['assetname'],
                                                                               row['asset'], row['holding'])
                        self.logger.debug('Insert sql: ' + sql)
                        cursor.execute(sql)
                        conn.commit()
                    sql = 'DELETE FROM OUTER_future_asset'
                    self.logger.debug('Delete sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
                    sql = 'INSERT INTO OUTER_future_asset ' \
                          '(business_date, fundname, assetname, asset, holding, risk_ratio) ' \
                          'SELECT business_date, fundname, assetname, asset, holding, ' \
                          'CASE WHEN asset > 0 THEN round( holding / asset * 100, 2 ) ELSE 0 END risk_ratio ' \
                          'FROM(' \
                          'SELECT ta.business_date, ta.fund_name fundname, ta.asset_name assetname,' \
                          'oi.holding, ta.total_value asset ' \
                          'FROM tassetasset ta, OUTER_imp_future_asset oi ' \
                          'WHERE 1=1 AND ta.fund_name = oi.fundname AND ta.asset_name = oi.assetname ' \
                          'AND ta.business_date = oi.business_date ) a'
                    self.logger.debug('Insert sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()

                # 3 账户层数据生成
                # 这里资金层数据有问题，如果是历史，单元的holding都是账户层的，用max
                # 如果是当天，单元的holding就是单元层的，用sum
                if self.base_date != datetime.datetime.now().strftime("%Y%m%d"):
                    sql = 'SELECT fund_name, account_name, asset, holding_margin, holding_margin-margin+new_margin new_holding_margin, ' \
                          'round(holding_margin/asset*100,2) ori_risk_ratio, ' \
                          'round((holding_margin-margin+new_margin)/asset*100,2) new_risk_ratio, ' \
                          'round((holding_margin - margin + three_margin)/(asset + three_profit)*100,2) three_risk_ratio, ' \
                          'round(three_profit,2) three_profit, ' \
                          'round((holding_margin - margin + five_margin)/(asset + five_profit)*100,2) five_risk_ratio, ' \
                          'round(five_profit,2) five_profit, ' \
                          'round((holding_margin - margin + eight_margin)/(asset + eight_profit)*100,2) eight_risk_ratio, ' \
                          'round(eight_profit,2) eight_profit ' \
                          'FROM' \
                          '(SELECT max(n.fund_name) fund_name, max(CONCAT(tcc.capital_account_name,\'_\',tcc.broker_name)) account_name, ' \
                          'sum(n.asset) asset, max(n.holding) holding_margin, sum(m.margin) margin, sum(m.new_margin) new_margin, ' \
                          'sum(m.three_margin) three_margin, sum(m.three_profit) three_profit, ' \
                          'sum(m.five_margin) five_margin, sum(m.five_profit) five_profit, ' \
                          'sum(m.eight_margin) eight_margin, sum(m.eight_profit) eight_profit ' \
                          'from tcapitalaccount tcc, tassetcapital tac, ' \
                          '(SELECT a.business_date, a.fund_id, a.asset_id, sum(margin) margin, sum(new_margin) new_margin, ' \
                          'sum(three_margin) three_margin, sum(three_profit) three_profit, ' \
                          'sum(five_margin) five_margin, sum(five_profit) five_profit, ' \
                          'sum(eight_margin) eight_margin, sum(eight_profit) eight_profit ' \
                          'FROM OUTER_fund_margin_detail a ' \
                          'GROUP BY a.business_date, a.fund_id, a.asset_id)m,' \
                          '(SELECT DISTINCT tus.fund_id, tus.fund_name, tus.asset_id, tus.asset_name, tfa.asset, tfa.holding, tfa.risk_ratio ' \
                          'FROM OUTER_future_asset tfa, tunitstock tus ' \
                          'WHERE tus.fund_name = tfa.fundname and tus.asset_name = tfa.assetname and tus.business_date = {0})n ' \
                          'where m.asset_id = n.asset_id and n.asset_id = tac.asset_id and tac.capital_account_id = tcc.capital_account_id ' \
                          'GROUP BY tcc.capital_account_id)b ' \
                          'ORDER BY fund_name ,account_name'.format(self.base_date)
                else:
                    sql = 'SELECT fund_name, account_name, asset, holding_margin, holding_margin-margin+new_margin new_holding_margin, ' \
                          'round(holding_margin/asset*100,2) ori_risk_ratio, ' \
                          'round((holding_margin-margin+new_margin)/asset*100,2) new_risk_ratio, ' \
                          'round((holding_margin - margin + three_margin)/(asset + three_profit)*100,2) three_risk_ratio, ' \
                          'round(three_profit,2) three_profit, ' \
                          'round((holding_margin - margin + five_margin)/(asset + five_profit)*100,2) five_risk_ratio, ' \
                          'round(five_profit,2) five_profit, ' \
                          'round((holding_margin - margin + eight_margin)/(asset + eight_profit)*100,2) eight_risk_ratio, ' \
                          'round(eight_profit,2) eight_profit ' \
                          'FROM' \
                          '(SELECT max(n.fund_name) fund_name, max(CONCAT(tcc.capital_account_name,\'_\',tcc.broker_name)) account_name, ' \
                          'sum(n.asset) asset, sum(n.holding) holding_margin, sum(m.margin) margin, sum(m.new_margin) new_margin, ' \
                          'sum(m.three_margin) three_margin, sum(m.three_profit) three_profit, ' \
                          'sum(m.five_margin) five_margin, sum(m.five_profit) five_profit, ' \
                          'sum(m.eight_margin) eight_margin, sum(m.eight_profit) eight_profit ' \
                          'from tcapitalaccount tcc, tassetcapital tac, ' \
                          '(SELECT a.business_date, a.fund_id, a.asset_id, sum(margin) margin, sum(new_margin) new_margin, ' \
                          'sum(three_margin) three_margin, sum(three_profit) three_profit, ' \
                          'sum(five_margin) five_margin, sum(five_profit) five_profit, ' \
                          'sum(eight_margin) eight_margin,sum(eight_profit) eight_profit ' \
                          'FROM OUTER_fund_margin_detail a ' \
                          'GROUP BY a.business_date, a.fund_id, a.asset_id)m,' \
                          '(SELECT DISTINCT tus.fund_id, tus.fund_name, tus.asset_id, tus.asset_name, tfa.asset, tfa.holding, tfa.risk_ratio ' \
                          'FROM OUTER_future_asset tfa, tunitstock tus ' \
                          'WHERE tus.fund_name = tfa.fundname and tus.asset_name = tfa.assetname and tus.business_date = {0})n ' \
                          'where m.asset_id = n.asset_id and n.asset_id = tac.asset_id and tac.capital_account_id = tcc.capital_account_id ' \
                          'GROUP BY tcc.capital_account_id)b ' \
                          'ORDER BY fund_name ,account_name'.format(self.base_date)
                self.logger.debug('Select sql: ' + sql)
                df = pd.DataFrame(pd.read_sql_query(sql, conn))
                makeup_line = 0.8
                df[str(makeup_line*100) + '%makeup'] = 0
                df[str(makeup_line*100) + '%makeup'] = 1 / makeup_line * df['new_holding_margin'].loc[df['new_risk_ratio'] >= 80] - df['asset'].loc[df['new_risk_ratio'] >= 80]
                self.logger.info('raising ratio detail result')
                self.logger.info('{0}'.format(df))
                filename = os.path.join(excel_out_path, '{0}提保结果.xlsx'.format(self.base_date))
                df.to_excel(filename)
                self.logger.info('Output excel file [{0}] with raising ratio result'.format(filename))
            finally:
                cursor.close()
                conn.close()


logger = dunhe_public.SetLog('RaiseDepositRatio')
cal_date = datetime.datetime.now().strftime("%Y%m%d")
cal_date = '20190927'
raiser = RaiseDepositRatio(logger, cal_date)
# raiser.get_current_ratio('G:\\data\\RaiseRatio')
# raiser.import_new_ratio_with_ratio_share('G:\\data\\RaiseRatio\\raise_ratio_with_ratio_share.xlsx')
# raiser.import_new_ratio_with_fix_ratio('G:\\data\\RaiseRatio\\raise_ratio_with_fix_ratio.xlsx')
# raiser.GenerateAccountRaiseTable('G:\\data\\RaiseRatio\\期货资产查询_20190425.xls', 'G:\\data\\RaiseRatio\\', only_select=True)
raiser.generate_account_raise_table('G:\\data\\RaiseRatio\\期货资产查询_20190927.xls', 'G:\\data\\RaiseRatio\\')
