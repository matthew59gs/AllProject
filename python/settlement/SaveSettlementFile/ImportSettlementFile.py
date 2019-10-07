# -*- coding:utf-8 -*-

import pymysql
import pandas as pd
import os
from simpledbf import Dbf5
import re
import zipfile
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public

class ImportSettlementFile:
    def __init__(self, logger, pathtable=None):
        self.logger = logger
        if pathtable:
            self.SetProductPath(pathtable)
        else:
            self.pathtable = None

    # pathtable 格式：
    # MAC, fund_code, import_file_type, broker, path
    # 机器MAC，产品代码，导入文件类型，文件所属证券公司，路径
    # MAC格式：AABBCCDDEEFF
    # 导入文件类型：1-估值表，2-预估值，3-证券结算文件，4-期货结算文件，5-期权结算文件
    # 文件所属证券公司：证券公司中文名称
    # 路径：绝对路径
    def set_product_path(self, pathtable=None):
        localmac = dunhe_public.GetLocalMac(separater='')
        self.logger.info('Local MAC is {0}'.format(localmac))
        if pathtable:
            self.pathtable = pd.DataFrame(pathtable.loc[pathtable['MAC'] == localmac, ['MAC', 'fund_code', 'import_file_type', 'broker', 'path']]).copy()
        else:
            try:
                conn = pymysql.connect(host='192.168.40.202', port=3306,
                                       user='risk', password='risk', db='risk', charset='utf8')
            except Exception as e:
                if self.logger:
                    self.logger.error("Sever connect fail: {0}".format(e))
                raise e
            else:
                try:
                    sql = 'select MAC, fund_code, import_file_type, broker, path from tsettlementfilepath'
                    self.logger.debug('Select sql: ' + sql)
                    df = pd.read_sql(sql=sql, con=conn)
                    self.logger.debug('MAC table info:\n{0}'.format(df))
                    self.pathtable = pd.DataFrame(df.loc[df['MAC'] == localmac, ['MAC', 'fund_code', 'import_file_type', 'broker', 'path']]).copy()
                finally:
                    conn.close()

    def show_import_path(self):
        if len(self.pathtable) > 0:
            self.logger.info(self.pathtable)
        else:
            self.logger.info('Path table is empty!')

    #导入上交所的港股通汇率表
    def import_HKD_exchange_rate(self, path):
        if path is None or path.strip() == '':
            return
        df = pd.DataFrame(pd.read_excel(path))
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                for iter,row in df.iterrows():
                    business_date = int(dunhe_public.conver_number2date(row['适用日期']))
                    sql = 'delete from texchange where business_date = {0}'.format(business_date)
                    self.logger.debug('delete sql: ' + sql)
                    cursor.execute(sql)
                    sql = 'insert texchange(business_date, settle_buy_exchange, settle_sale_exchange, currency) ' \
                          'values ({0}, {1}, {2}, \'{3}\')'.format(business_date, row['买入结算汇兑比率'], row['卖出结算汇兑比率'], row['货币种类'])
                    self.logger.debug('insert sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
                self.logger.info('Import exchange file ' + path)
            finally:
                cursor.close()
                conn.close()

    def import_file(self):
        if len(self.pathtable) == 0:
            self.logger('路径表为空，不能导入文件！')
            return

        for index, row in self.pathtable.iterrows():
            path = row['path']
            file_type = row['import_file_type']
            fund_code = row['fund_code']
            broker = row['broker']
            #股票都是excel文件
            if file_type == 3:
                desdir = os.path.join(path, 'Done')
                if not os.path.exists(desdir):
                    os.makedirs(desdir)
                for files in os.listdir(path):
                    if files.find('.') >= 0:
                        suffix = files.split('.')[1]
                        if suffix.lower() == 'xlsx' or suffix.lower() == 'xls':
                            self.logger.info('Import stock file ' + files)
                            self.__import_stock_file(path=os.path.join(path, files), fund_code=fund_code, broker=broker)
                            os.rename(os.path.join(path, files), os.path.join(desdir, files))
            #期货都是压缩包，要解压
            if file_type == 4:
                self.__import_future_file(path=path, fund_code=fund_code, broker=broker)
            #期权都是excel文件
            if file_type == 5:
                desdir = os.path.join(path, 'Done')
                if not os.path.exists(desdir):
                    os.makedirs(desdir)
                for files in os.listdir(path):
                    if files.find('.') >= 0:
                        suffix = files.split('.')[1]
                        if suffix.lower() == 'xlsx' or suffix.lower() == 'xls':
                            self.logger.info('Import option file ' + files)
                            self.__import_option_file(path=os.path.join(path, files), fund_code=fund_code, broker=broker)
                            os.rename(os.path.join(path, files), os.path.join(desdir, files))

    def __import_stock_file(self, path, fund_code, broker):
        df = pd.DataFrame(pd.read_excel(path))
        business_date = 0
        i_cap_start = 0
        i_cap_end = 0
        i_deal_start = 0
        i_deal_end = 0
        i_hold_start = 0
        i_hold_end = 0
        capital_account = ''
        for index, row in df.iterrows():
            if not pd.isnull(row[0]):
                if business_date == 0 and row[0].find(r'起止日期') == 0:
                    business_date = ''.join(re.findall(r'起止日期：(\d+)年(\d+)月(\d+)日', row[0])[0])
                elif row[0] == r'资金情况':
                    i_cap_start = index + 1
                elif row[0] == r'对帐单':
                    i_deal_start = index + 1
                elif row[0] == r'当日持仓清单':
                    i_hold_start = index + 1
            else:
                if i_cap_start > 0 and i_cap_end == 0:
                    i_cap_end = index
                elif i_deal_start > 0 and i_deal_end == 0:
                    i_deal_end = index
                elif i_hold_start > 0 and i_hold_end == 0:
                    i_hold_end = index
        if i_cap_start > 0:
            self.logger.debug('Capital start[{0}] end[{1}]'.format(i_cap_start, i_cap_end))
            capital_account = self.__import_capital(df=df[i_cap_start:i_cap_end].copy(), business_date=business_date,
                                                    fund_code=fund_code, broker=broker)
            self.logger.info('Add fund[{0}]account[{1}] with date[{2}] capital info'.format(fund_code, capital_account,
                                                                                       business_date))
        if i_deal_start > 0 and capital_account != '':
            self.logger.debug('Deal start[{0}] end [{1}]'.format(i_deal_start, i_deal_end))
            count = self.__import_deal(df[i_deal_start:i_deal_end].copy(), business_date=business_date,
                                       fund_code=fund_code, capital_account=capital_account)
            self.logger.info('Add fund[{0}]account[{1}] with date[{2}][{3}] deal info'.format(fund_code, capital_account,
                                                                                         business_date, count))
        if i_hold_start > 0:
            self.logger.debug('Hold start[{0}] end [{1}]'.format(i_hold_start, i_hold_end))
            count = self.__import_hold(df[i_hold_start:i_hold_end].copy(), business_date=business_date,
                                       fund_code=fund_code, capital_account=capital_account)
            self.logger.info('Add fund[{0}]account[{1}] with date[{2}][{3}] hold info'.format(fund_code, capital_account,
                                                                                         business_date, count))

    def __import_capital(self, df, business_date, fund_code, broker):
        df.index = range(len(df))
        df_cap = df[1:len(df)]
        df_cap.columns = list(df.loc[0].values)
        capital_account = ''
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                for index, row in df_cap.iterrows():
                    capital_account = row['资产账户']
                    sql = 'delete from tcapital_settlement where business_date = {0} and account = \'{1}\' ' \
                          'and broker = \'{2}\' and fund_code = \'{3}\''.format(
                        business_date, capital_account, broker, fund_code)
                    self.logger.debug('Delete sql:' + sql)
                    cursor.execute(sql)
                    sql = 'insert into tcapital_settlement' \
                          '(business_date, fund_code, account, equity, account_type, broker, capital_type) ' \
                          'values({0}, \'{1}\', \'{2}\', {3}, {4}, \'{5}\', {6})'.format(
                        business_date, fund_code, capital_account, row['资金余额'], 1, broker, 3)
                    self.logger.debug('Insert sql: ' + sql)
                    cursor.execute(sql)
                    sql = 'insert into tcapital_settlement' \
                          '(business_date, fund_code, account, equity, account_type, broker, capital_type) ' \
                          'values({0}, \'{1}\', \'{2}\', {3}, {4}, \'{5}\', {6})'.format(business_date, fund_code, capital_account, row['总资产'], 1, broker, 1)
                    self.logger.debug('Insert sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
            finally:
                cursor.close()
                conn.close()

        return capital_account

    def __import_deal(self, df, business_date, fund_code, capital_account):
        count = 0
        #中信结算文件的成交部分如果有效，至少是4行
        if len(df) < 4:
            return count
        df.index = range(len(df))
        df_deal = df[2:len(df)]
        df_deal.columns = list(df.loc[0].values)
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                sql = 'delete from tdeal_settlement where business_date = {0} and account = \'{1}\' and fund_code = \'{2}\''.format(
                    business_date, capital_account, fund_code)
                self.logger.debug('Delete sql:' + sql)
                cursor.execute(sql)
                for index, row in df_deal.iterrows():
                    if len(re.findall('\d+', row['发生日期'])) == 0:
                        continue
                    stock_type = self.__get_stock_type_by_stock(date=row['发生日期'], stock=row['证券代码'])
                    sql = 'insert into tdeal_settlement' \
                          '(business_date, fund_code, account, report_code, deal_amount, deal_price, ' \
                          'deal_balance, business_type, business, stock_type) ' \
                          'values({0}, \'{1}\', \'{2}\', \'{3}\', {4}, {5}, {6}, \'{7}\', \'{8}\', {9})'.format(
                        row['发生日期'], fund_code, capital_account, row['证券代码'], row['成交股数'], row['成交价格'],
                        row['发生金额'], row['摘要'], row['摘要'], stock_type)
                    self.logger.debug('Insert sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
                    count = count + 1
            finally:
                cursor.close()
                conn.close()
        return count

    def __get_stock_type_by_stock(self, date, stock):
        if pd.isnull(stock) or stock is None or stock.strip() == '':
            return 0
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='oplus', password='oplus', db='oplus_p', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                sql = 'SELECT stock_type FROM `tstockinfo_stock` t WHERE t.report_code = \'{0}\' and t.business_date = {1}'.format(stock, date)
                self.logger.debug('select sql: ' + sql)
                cursor.execute(sql)
                data = cursor.fetchone()
                if data == None or len(data) == 0:
                    #港股不在Oplus数据库里面，长度是5，所以这里就返回1
                    if len(stock) == 5:
                        return '1'
                else:
                    return data[0]
            finally:
                cursor.close()
                conn.close()
        return 0

    def __import_hold(self, df, business_date, fund_code, capital_account):
        count = 0
        # 中信结算文件的持仓部分如果有效，至少是3行
        if len(df) < 3:
            return count
        df.index = range(len(df))
        df_hold = df[1:len(df)]
        df_hold.columns = list(df.loc[0].values)
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                sql = 'delete from thold_settlement where business_date = {0} and account = \'{1}\' and fund_code = \'{2}\''.format(
                    business_date, capital_account, fund_code)
                self.logger.debug('Delete sql:' + sql)
                cursor.execute(sql)
                for index, row in df_hold.iterrows():
                    if row['股东帐号'] == r'合计：':
                        continue
                    sql = 'insert into thold_settlement ' \
                          '(business_date, fund_code, account, report_code, ' \
                          'rest_amount, available_amount, frozen_amount, ' \
                          'cost, cost_price, value_price, total_value) ' \
                          'values({0},\'{1}\',\'{2}\',\'{3}\',{4},{5},{6},{7},{8},{9},{10})'.format(
                        business_date, fund_code, capital_account, row['证券代码'],
                        row['股份余额'], row['股份可用'], row['交易冻结'],
                        row['参考成本'], row['参考成本价'], row['参考市价'], row['参考市值'])
                    self.logger.debug('Insert sql: ' + sql)
                    cursor.execute(sql)
                    conn.commit()
                    count = count + 1
            finally:
                cursor.close()
                conn.close()
        return count

    def __import_future_file(self, path, fund_code, broker):
        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                sql = 'SELECT data_file_type FROM `tsettlementfilepath` t WHERE t.import_file_type = 4 and t.fund_code = \'{0}\''.format(fund_code)
                cursor.execute(sql)
                data = cursor.fetchone()
                if len(data) > 0:
                    data_file_type = '.' + data[0]
                else:
                    return
                movedir = os.path.join(path, 'Done')
                if not os.path.exists(movedir):
                    os.makedirs(movedir)
                for files in os.listdir(path):
                    if files.upper().find('.RAR') > 0:
                        filename = files.split('.')[0]
                        desdir = os.path.join(path, filename)
                        if not os.path.exists(desdir):
                            os.makedirs(desdir)
                        os.chdir(path)
                        dunhe_public.unrarfile(files, desdir)
                        for rarfiles in os.listdir(desdir):
                            if rarfiles.find('Capital.dbf') > 0:
                                date = dunhe_public.GetDateByString(rarfiles)
                                dbf = Dbf5(os.path.join(desdir, rarfiles), codec='GBK')
                                table = pd.DataFrame(dbf.to_dataframe())
                                account = table.iloc[0, 0]
                                value = table.loc[table['ITEMDESC'] == '当日实有货币资金余额', ['ITEMVALUE']]
                                for index, row in value.iterrows():
                                    sql = 'delete from tcapital_settlement where business_date = {0} and fund_code = \'{1}\' ' \
                                          'and account = \'{2}\''.format(date, fund_code, account)
                                    self.logger.debug('delete sql: ' + sql)
                                    cursor.execute(sql)
                                    sql = 'insert into tcapital_settlement(business_date, fund_code, account, ' \
                                          'equity, account_type, broker, capital_type) values(' \
                                          '{0},\'{1}\',\'{2}\',{3},{4},\'{5}\',{6})'.format(
                                        date, fund_code, account, row['ITEMVALUE'], 2, broker, 1)
                                    self.logger.debug('insert sql: ' + sql)
                                    cursor.execute(sql)
                                    conn.commit()
                                    self.logger.info('Add fund[{0}]account[{1}] with date[{2}] capital info'.format(
                                        fund_code, account, date))
                    elif files.upper().find('.ZIP') > 0:
                        filename = files.split('.')[0]
                        self.logger.info('Import future file ' + files)
                        os.chdir(path)
                        extracting = zipfile.Zipfile(files)
                        zipfilepath = os.path.join(path, filename)
                        extracting.extractall(zipfilepath)
                        for one_file in extracting.namelist():
                            if one_file.upper().find(data_file_type) > 0:
                                if data_file_type == '.DBF':
                                    self.__import_future_dbf(path=zipfilepath, fund_code=fund_code, broker=broker)
                                elif data_file_type == '.TXT':
                                    self.__import_future_txt(path=zipfilepath, fund_code=fund_code, broker=broker)
                    elif files.upper().find(data_file_type) > 0:
                        filepath = os.path.join(path, filename)
                        if data_file_type == '.DBF':
                            self.__import_future_dbf(path=filepath, fund_code=fund_code, broker=broker)
                        elif data_file_type == '.TXT':
                            self.__import_future_txt(path=filepath, fund_code=fund_code, broker=broker)
                os.rename(os.path.join(path, files), os.path.join(movedir, files))
            finally:
                cursor.close()
                conn.close()

        return

    def __import_option_file(self, path, fund_code, broker):
        df = pd.DataFrame(pd.read_excel(path))
        business_date = 0
        i_cap_start = 0
        i_cap_end = 0
        capital_account = ''
        value = 0
        for index, row in df.iterrows():
            if not pd.isnull(row[0]):
                if business_date == 0 and row[0].find(r'起止日期') == 0:
                    business_date = ''.join(re.findall(r'起止日期：(\d+)年(\d+)月(\d+)日', row[0])[0])
                elif row[0] == r'客户编号:':
                    i_cap_start = index
            else:
                if i_cap_start > 0 and i_cap_end == 0:
                    i_cap_end = index
        if i_cap_start > 0:
            self.logger.debug('Capital start[{0}] end[{1}]'.format(i_cap_start, i_cap_end))
            df_cap = df[i_cap_start:i_cap_end].copy()
            for index, row in df_cap.iterrows():
                if row[0] == r'资产账户:':
                    capital_account = row[1]
                if row[0] == r'总权益：':
                    value = row[1]
                    break
            if capital_account != '' and value != 0:
                try:
                    conn = pymysql.connect(host='192.168.40.202', port=3306,
                                           user='risk', password='risk', db='risk', charset='utf8')
                except Exception as e:
                    if self.logger:
                        self.logger.error("Sever connect fail: {0}".format(e))
                    raise e
                else:
                    try:
                        cursor = conn.cursor()
                        sql = 'delete from tcapital_settlement where business_date = {0} and account = \'{1}\' ' \
                              'and broker = \'{2}\' and fund_code = \'{3}\''.format(
                            business_date, capital_account, broker, fund_code)
                        self.logger.debug('Delete sql:' + sql)
                        cursor.execute(sql)
                        sql = 'insert into tcapital_settlement' \
                              '(business_date, fund_code, account, equity, account_type, broker, capital_type) ' \
                              'values({0}, \'{1}\', \'{2}\', {3}, {4}, \'{5}\', {6})'.format(
                            business_date, fund_code, capital_account, value, 3, broker, 1)
                        self.logger.debug('Insert sql: ' + sql)
                        cursor.execute(sql)
                        conn.commit()
                    finally:
                        cursor.close()
                        conn.close()
                self.logger.info('Add fund[{0}] option account[{1}] with date[{2}] capital info'.format(fund_code,
                                                                                                   capital_account,
                                                                                                   business_date))

    def __import_future_dbf(self, path, fund_code, broker):
        [dirname, filename]=os.path.split(path)
        delete_sql = ''
        insert_sql_list = []
        self.logger.info('Import future file ' + filename)

        try:
            conn = pymysql.connect(host='192.168.40.202', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            if self.logger:
                self.logger.error("Sever connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = conn.cursor()
                sql = 'SELECT DISTINCT t.dbf_key from tdbf_match t GROUP BY t.dbf_key;'
                df_dbf_key = pd.DataFrame(pd.read_sql(sql, conn))
                sql = 'SELECT t.DBF_key, t.DBF_type, t.match_table, t.DBF_sub, t.table_sub, t.memo FROM tdbf_match t'
                df_dbf_sub_all = pd.DataFrame(pd.read_sql(sql, conn))
                for index, row in df_dbf_key.iterrows():
                    if filename.upper().find(row['dbf_key']) > 0:
                        date = dunhe_public.GetDateByString(filename)
                        dbf = Dbf5(path, codec='GBK')
                        table = pd.DataFrame(dbf.to_dataframe())
                        df_sub = df_dbf_sub_all.loc[df_dbf_sub_all['DBF_key'].trim() == row['dbf_key']]
                        if row['memo'] == r'整个DBF对应一条数据':

                        else:

                date = dunhe_public.GetDateByString(filename)
                dbf = Dbf5(path, codec='GBK')
                table = pd.DataFrame(dbf.to_dataframe())
                if filename.upper().find('Capital.DBF') > 0:
                    account = table.iloc[0, 0]
                    last_equity = self.__get_future_capital_value(desc='上一交易日实有货币资金余额', table=table)
                    equity = self.__get_future_capital_value(desc='当日实有货币资金余额', table=table)
                    margin = self.__get_future_capital_value(desc='其中：交易保证金', table=table)
                    in_cash = self.__get_future_capital_value(desc='加：当日收入资金', table=table)
                    out_cash = self.__get_future_capital_value(desc='减：当日付出资金', table=table)
                    fee = self.__get_future_capital_value(desc='应收手续费', table=table)
                    delete_sql = 'delete from tfuture_capital where business_date = {0} and fund_code = \'{1}\' ' \
                                 'and account = \'{2}\''.format(date, fund_code, account)
                    insert_sql = 'insert into tfuture_capital(business_date, fund_code, account, ' \
                                 'last_equity, equity, margin, in_cash, out_cash, fee) values(' \
                                 '{0},\'{1}\',\'{2}\',{3},{4},{5},{6},{7},{8})'.format(
                        date, fund_code, account,
                        last_equity, equity, margin, in_cash, out_cash, fee)
                    insert_sql_list.append(insert_sql)
                    self.logger.info('Add fund[{0}]account[{1}] with date[{2}] capital info'.format(
                        fund_code, account, date))
                elif filename.find('SettlementDetail.DBF') > 0:
                    delete_sql = 'delete from tfuture_holding where business_date = {0} ' \
                                 'and fund_code = \'{1}\' '.format(date, fund_code)
                    for index, row in table.iterrows():
                        stockholder = row['Clientid']
                        report_code = row['Instrid']
                        settle_price = row['Clearprice']
                        long_amount = row['Btotalamt']
                        short_amount = row['Stotalamt']
                        margin = row['Margin']
                        daily_holding_profit = row['Actual']
                        insert_sql = 'insert into tfuture_holding(business_date, fund_code, report_code, stockholder, ' \
                                     'long_amount, short_amount, margin, daily_holding_profit, settle_price) values(' \
                                     '{0},\'{1}\',\'{2}\',\'{3}\',' \
                                     '{4},{5},{6},{7},{8})'.format(date, fund_code, report_code, stockholder,
                                                                   long_amount, short_amount, margin,
                                                                   daily_holding_profit, settle_price)
                        insert_sql_list.append(insert_sql)
                elif filename.find('Trade.DBF') > 0:
                    delete_sql = 'delete from tfuture_deal where business_date = {0} ' \
                                 'and fund_code = \'{1}\' '.format(date, fund_code)
                    for index, row in table.iterrows():
                        insert_sql = ''
                        insert_sql_list.append(insert_sql)

                if delete_sql != '':
                    self.logger.debug('delete sql: ' + delete_sql)
                    cursor.execute(delete_sql)
                if len(insert_sql_list) > 0:
                    for insert_sql in insert_sql_list:
                        self.logger.debug('insert sql: ' + insert_sql)
                        cursor.execute(insert_sql)
                        conn.commit()
            finally:
                cursor.close()
                conn.close()


    def __get_future_capital_value(self, src_sub ='', des_sub = '', describe='', table=None):
        if src_sub == '' or des_sub == '' or describe == '':
            return
        else:
            value = table.loc[table[src_sub].trim() == describe, [des_sub]]
            for index, row in value.iterrows():
                return row[des_sub]

    def __import_future_txt(self, path, fund_code, broker):
        return


