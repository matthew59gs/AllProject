#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 从Oplus读取取当日市场数据
# 从Oplus读取当日持仓数据
# tradesplit库做表汇总分析，形成Excel

import pymysql
import datetime
import os
#import sys
#sys.path.append("..\\..\\public\\python")
#import dunhe_public
import pandas
import enum

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns',500)
pandas.set_option('display.width',1000)
hq_holding_data_filename = 'hq_holding_data.xlsx'
hq_data_filename = 'hq_data.xlsx'
holding_data_finename = 'holding_data.xlsx'
detail_data_filename = 'detail_data.xlsx'


class DemensionType(enum.IntEnum):
    Company = 1,
    Manager = 2,
    StockManager = 3,
    FutureManager = 4,
    Fund = 5


class HQReceiver:
    def __init__(self, logger):
        self.logger = logger

    def GetMarketData(self, I_hqdate = datetime.datetime.now().strftime("%Y%m%d")):
        try:
            mysql_conn = pymysql.connect(host='192.168.40.202', port=3306, user='oplus', 
                                    password='oplus', db='oplus_p',charset='utf8')
        except Exception as e:
            self.logger.error("mysql connect fail: {0}".format(e))
            raise e
        else:
            cursor = mysql_conn.cursor()
            try:
                sql = 'SELECT \
                    t.report_code report_code, \
                    tfk.future_kind_code future_kind_code, \
                    t.market_no market_no, \
                    t.business_date business_date, \
                    t.position_quantity / 2 position_quantity \
                FROM \
                    tstockinfo_future t, tfuturekind tfk \
                WHERE \
                    t.future_kind_id = tfk.future_kind_id \
                    AND t.business_date = \'{0}\'  \
                    AND t.position_quantity > 0  \
                    AND t.market_no IN ( \'3\', \'4\', \'9\', \'34\' ) UNION ALL \
                SELECT \
                    t.report_code report_code, \
                    tfk.future_kind_code future_kind_code, \
                    t.market_no, \
                    t.business_date, \
                    t.position_quantity  \
                FROM \
                    tstockinfo_future t, tfuturekind tfk \
                WHERE \
                    t.future_kind_id = tfk.future_kind_id \
                    and t.business_date = \'{0}\'  \
                    AND t.position_quantity > 0  \
                    AND t.market_no IN ( \'7\' )'.format(I_hqdate)
                self.logger.debug('select sql: ' + sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                self.logger.info('Get {0} data from market'.format(len(data)))
                title = []
                for field_desc in cursor.description:
                    title.append(field_desc[0])
                dataset_hq = pandas.DataFrame(list(data), columns = title)
                self.logger.debug('Dataset HQ2: {0}'.format(dataset_hq))
                return dataset_hq
            except Exception as e:
                self.logger.error("Sql execute error: {0}".format(e))
                raise e
            finally:
                cursor.close()
                mysql_conn.close()

class BasicHoldingReceiver:
    def __init__(self, logger):
        self.logger = logger

    def GetHoldingData(self, I_holdingdate):
        try:
            mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
                                         user='oplus', password='oplus',
                                         db='oplus_p',
                                         charset='utf8')
        except Exception as e:
            self.logger.error("mysql connect fail: {0}".format(e))
            raise e
        else:
            cursor = mysql_conn.cursor()
            try:
                sql = 'SELECT DISTINCT  \
                    tf.fund_id, \
                    tf.fund_code fund_code, \
                    tf.fund_name, \
                    tfs.business_date business_date,  \
                    tfk.future_kind_code future_kind_code,  \
                    tfs.report_code report_code,  \
                    tfs.position_type,  \
                    tfs.current_amount \
                FROM  \
                  tfund tf, \
                    tfundstock tfs,  \
                    tfuturekind tfk,  \
                    tstockinfo_future tsf   \
                WHERE  \
                  1 = 1 \
                    AND tf.fund_id = tfs.fund_id \
                    AND tfs.report_code = tsf.report_code   \
                    AND tsf.future_kind_id = tfk.future_kind_id   \
                    AND tfs.business_date = {0}   \
                    AND tfs.market_no IN ( \'3\', \'4\', \'7\', \'9\', \'34\' )   \
                    AND tfs.position_type IN ( \'1\', \'2\' )   \
                    AND tfs.current_amount > 0  \
                ORDER BY tf.fund_id;'.format(I_holdingdate)
                self.logger.debug('select sql: ' + sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                self.logger.info('Get {0} data from oplus'.format(len(data)))
                title = []
                for field_desc in cursor.description:
                    title.append(field_desc[0])
                dataset_holding = pandas.DataFrame(list(data), columns = title)
            except Exception as e:
                self.logger.error("Sql execute error: {0}".format(e))
                raise e
            finally:
                cursor.close()
                mysql_conn.close()

        try:
            mysql_conn = pymysql.connect(host='192.168.40.202', port=3306,
                                         user='trader', password='123456',
                                         db='MailSaver',
                                         charset='utf8')
        except Exception as e:
            self.logger.error("mysql connect fail: {0}".format(e))
            raise e
        else:
            try:
                cursor = mysql_conn.cursor()
                sql = 'SELECT \
                    t.FundCode fund_code, \
                    t.FundName, \
                    t.Manager, \
                    t.SubManagerStock, \
                    t.SubManagerFuture  \
                FROM \
                    FundInfo_ALL t  \
                WHERE \
                    1 = 1  \
                    AND t.Valid = \'1\'  \
                    AND t.SubManagerFuture IS NOT NULL;'
                self.logger.debug('select sql: ' + sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                title = []
                for field_desc in cursor.description:
                    title.append(field_desc[0])
                dataset_fundinfo = pandas.DataFrame(list(data), columns = title)
            except Exception as e:
                self.logger.error("Sql execute error: {0}".format(e))
                raise e
            finally:
                cursor.close()
                mysql_conn.close()

        dataset = pandas.merge(dataset_holding, dataset_fundinfo, on = 'fund_code', how = 'left')
        self.logger.debug('dataset: {0}'.format(dataset))
        
        return dataset

class DataMerge:
    def __init__(self, logger, dataset_holding, dataset_hq):
        self.logger = logger
        self.dataset_holding = dataset_holding
        self.dataset_hq = dataset_hq
    
    def MergerHqDataAndHoldingData(self, dimensions = DemensionType.Company):
        #行情默认字段
        #report_code	future_kind_code	market_no	business_date	position_quantity
        #行情处理成两份，一份是原先的合约的去掉一些信息，一份是按照品种汇总的
        #hq_contract_data = self.dataset_hq.copy()
        #hq_contract_data.rename(columns={'position_quantity':'contract_quantity'}, inplace = True)
        #if 'Unnamed: 0' in hq_contract_data.columns:
        #    hq_contract_data.drop(columns=['Unnamed: 0'], inplace = True)
        #hq_contract_data.drop(columns=['future_kind_code', 'market_no', 'business_date'], inplace = True)
        
        hq_data1 = self.dataset_hq.copy()
        hq_data1.rename(columns={'position_quantity':'contract_quantity'}, inplace = True)
        hq_contract_data = hq_data1.groupby('report_code').agg({'contract_quantity':'mean'})
        
        hq_data2 = self.dataset_hq.copy()
        hq_data2.rename(columns={'position_quantity':'future_kind_quantity'}, inplace = True)
        hq_future_kind_data = hq_data2.groupby('future_kind_code').agg({'future_kind_quantity':'sum'})

        
        data00 = self.dataset_holding.copy()
        data00.rename(columns={'current_amount':'contract_amount'}, inplace = True)
        data01 = self.dataset_holding.copy()
        data01.rename(columns={'current_amount':'future_kind_amount'}, inplace = True)
        #持仓默认字段
        #fund_id	fund_code	fund_name	business_date	future_kind_code	report_code	position_type	current_amount	FundName	Manager	SubManagerStock	SubManagerFuture
        #持仓处理成两份，一份是按照合约的，一份是按照品种的
        if dimensions == DemensionType.Company:
            #data_contract = data00.groupby(['business_date', 'future_kind_code', 'report_code', 'position_type']).agg({ \
            #                              'future_kind_code':'last', 'report_code':'last', 'position_type':'last', 'contract_amount':'sum'})
            data_contract = data00.groupby(['future_kind_code', 'report_code', 'position_type']).agg({'contract_amount':'sum'})
            #data_future_kind = data01.groupby(['business_date', 'future_kind_code', 'position_type']).agg({'future_kind_code':'last', \
            #                                 'position_type':'last', 'future_kind_amount':'sum'})
            data_future_kind = data01.groupby(['future_kind_code', 'position_type']).agg({'future_kind_amount':'sum'})
            data_contract = data_contract.reset_index()
            data_future_kind = data_future_kind.reset_index()
            data_holding = pandas.merge(data_contract, data_future_kind, on = ['future_kind_code', 'position_type'], how = 'left')
        elif dimensions == DemensionType.Manager:
            data = 1
        elif dimensions == DemensionType.StockManager:
            data = 1
        elif dimensions == DemensionType.FutureManager:
            data_contract = data00.groupby(['future_kind_code', 'report_code', 'position_type', 'SubManagerFuture']).agg({'contract_amount':'sum'})
            data_future_kind = data01.groupby(['future_kind_code', 'position_type', 'SubManagerFuture']).agg({'future_kind_amount':'sum'})
            data_contract = data_contract.reset_index()
            data_future_kind = data_future_kind.reset_index()
            data_holding = pandas.merge(data_contract, data_future_kind, on = ['future_kind_code', 'position_type', 'SubManagerFuture'], how = 'left')
        elif dimensions == DemensionType.Fund:
            data = 1

        data_contract_holding = pandas.merge(data_holding, hq_contract_data, on = 'report_code', how = 'left')
        data = pandas.merge(data_contract_holding, hq_future_kind_data, on = 'future_kind_code', how = 'left')
        if type(data['position_type'][0]) == type('a'):
            data.loc[lambda data: data['position_type'] == '1', ['position_type']] = '多'
            data.loc[lambda data: data['position_type'] == '2', ['position_type']] = '空'
        else:
            data.loc[lambda data: data['position_type'] == 1, ['position_type']] = '多'
            data.loc[lambda data: data['position_type'] == 2, ['position_type']] = '空'
        data['contract_ratio'] = round(data['contract_amount'] / data['contract_quantity'] * 100, 2)
        data['future_kind_ratio'] = round(data['future_kind_amount'] / data['future_kind_quantity'] * 100, 2)

        if dimensions == DemensionType.Company:
            new_columns_list = ['position_type', 'future_kind_code', 'future_kind_amount', 'future_kind_quantity', \
                                'future_kind_ratio', 'report_code', 'contract_amount', 'contract_quantity', 'contract_ratio']
            data = data[new_columns_list]
            data = data.sort_values(by=['position_type', 'future_kind_code', 'report_code'], axis=0, ascending=True)
            output_string = 'Company'
        elif dimensions == DemensionType.Manager:
            output_string = 'Manager'
        elif dimensions == DemensionType.StockManager:
            output_string = 'StockManager'
        elif dimensions == DemensionType.FutureManager:
            data = data.sort_values(by=['position_type', 'future_kind_code', 'report_code'], axis=0, ascending=True)
            output_string = 'FutureManager'          
        elif dimensions == DemensionType.Fund:
            output_string = 'Fund'

        self.logger.debug('{0} aggregates data: {1}'.format(output_string, data))
        return data

    def OutputExcelDataWithDataframe(self, path, namelist, datalist):
        with pandas.ExcelWriter(os.path.join(path)) as writer:
            for i in range(0, len(namelist)):
                datalist[i].to_excel(writer, sheet_name = namelist[i])
        return None
