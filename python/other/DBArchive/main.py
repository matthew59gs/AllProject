# -*- coding:utf-8 -*-

import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import pymysql
import pandas as pd
import datetime

class DbArchiver:
    def __init__(self, logger):
        self.loggger = logger
        self.conn = None

    def __del__(self):
        if self.IsConnect():
            self.conn.close()

    def Connect(self):
        try:
            self.conn = pymysql.connect(host='192.168.40.202', port=3306,\
                                        user='oplus',password='oplus',db='oplus_p',charset='utf8')
            return True
        except Exception as e:
            self.loggger.error("Sever connect fail: {0}".format(e))
            return False

    def IsConnect(self):
        if self.conn:
            return self.conn.open
        else:
            return False

    def CheckHisTable(self):
        if self.IsConnect():
            sql = 'show tables'
            all_table = pd.DataFrame(pd.read_sql_query(sql, self.conn))
            all_table.columns = ['table']
            sql = 'select * from tarchive;'
            archive_list = pd.DataFrame(pd.read_sql_query(sql, self.conn))
            match_result = archive_list[~archive_list['his_table'].isin(all_table['table'])]
            if match_result['curr_table'].count() > 0:
                try:
                    cursor = self.conn.cursor()
                    for index, row in match_result.iterrows():
                        sql = 'create table {0} select * from {1} where 1 = 2'.format(row['his_table'], row['curr_table'])
                        self.loggger.debug('Create sql: ' + sql)
                        try:
                            cursor.execute(sql)
                            self.conn.commit()
                        except Exception as e:
                            self.loggger.error('Sql execute error: {0}'.format(e))
                        self.loggger.info('Create histable [{0}] from [{1}]'.format(row['his_table'], row['curr_table']))
                finally:
                    cursor.close()

    # def CheckHisTable(self):
    #     if self.IsConnect():
    #         sql = 'show tables'
    #         df = pd.DataFrame(pd.read_sql_query(sql, self.conn))
    #
    #         his_table = df.loc[df['Tables_in_oplus_p'].str.startswith('this')].copy()
    #         his_table.reindex()
    #         his_table.columns = ['his_table']
    #         his_table['cur_table'] = his_table['his_table'].str.replace('this', 't')
    #
    #         curr_table_ori = df.loc[df['Tables_in_oplus_p'].str.startswith('t')].copy()
    #         curr_table_ori.columns = ['cur_table']
    #         curr_table_no_his = curr_table_ori[~curr_table_ori['cur_table'].str.startswith('this')]
    #         curr_table = curr_table_no_his[~curr_table_no_his['cur_table'].isin(his_table['cur_table'])]
    #         #self.loggger.info(curr_table)
    #         curr_table['his_table'] = curr_table['cur_table']
    #         curr_table['his_table'].replace(inplace=True, regex={'^t': 'this'})
    #         self.loggger.debug('All table is:\n{0}\nCurrent table is:\n{1}\nHistable is \n{2}'.format(df, curr_table, his_table))
    #
    #         if curr_table['cur_table'].count() > 0:
    #             try:
    #                 cursor = self.conn.cursor()
    #                 for index, row in curr_table.iterrows():
    #                     sql = 'create table {0} select * from {1} where 1 = 2'.format(row['his_table'], row['cur_table'])
    #                     self.loggger.debug('Create sql: ' + sql)
    #                     try:
    #                         cursor.execute(sql)
    #                         self.conn.commit()
    #                     except Exception as e:
    #                         self.loggger.error('Sql execute error: {0}'.format(e))
    #                     self.loggger.info('Create his table [{0}] from [{1}]'.format(row['his_table'], row['cur_table']))
    #             finally:
    #                 cursor.close()
    #
    #         self.tablelist = pd.merge(curr_table, his_table, on = ['cur_table', 'his_table'], how = 'outer').copy()
    #         self.loggger.info('Arcive table list: {0}'.format(self.tablelist))

    def Archive(self, Timespan = 0, SpecifyDate = 0):
        if SpecifyDate != 0:
            specify_date = str(SpecifyDate - 1)
        else:
            if Timespan == 0:
                self.loggger.debug('Archive {0} days data'.format(Timespan))
                return
            else:
                specify_date = (datetime.datetime.now() - datetime.timedelta(days=Timespan)).strftime('%Y%m%d')

        if self.IsConnect():
            sql = 'select * from tarchive;'
            archive_list = pd.DataFrame(pd.read_sql_query(sql, self.conn))
            cursor = self.conn.cursor()
            try:
                for index, row in archive_list.iterrows():
                    try:
                        sql = 'insert into {0} select * from {1} where business_date <= {2}'.format(row['his_table'], row['curr_table'], specify_date)
                        self.loggger.debug('execute sql: ' + sql)
                        rows = cursor.execute(sql)
                        self.conn.commit()
                        sql = 'delete from {0} where business_date <= {1}'.format(row['curr_table'], specify_date)
                        self.loggger.debug('execute sql: ' + sql)
                        rows = cursor.execute(sql)
                        self.conn.commit()
                    except Exception as e:
                        self.conn.rollback()
                        self.loggger.error('Sql execute error: {0}'.format(e))
                    self.loggger.info('Archive table[{0}] with {1} data from {2}'.format(row['curr_table'], rows, specify_date))
            finally:
                cursor.close()

archiver = DbArchiver(dunhe_public.SetLog('DBArchive'))
archiver.Connect()
archiver.CheckHisTable()
archiver.Archive(Timespan=90)