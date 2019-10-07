# -*- condig: utf-8 -*-
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public
import pymysql
import pandas as pd
import os

FILENAME_SUM = 'Statistics_sum.xlsx'
FILENAME_DETAIL = 'Statistics_detail.xlsx'


class Statistics:
    def __init__(self, log):
        self.log = log

    def count_not_use_oplus_product(self, path='', period=''):
        try:
            # 数据库连接
            connection = pymysql.connect(host='192.168.40.202', port=3306,
                                         user='oplus', password='oplus', db='oplus_p', charset='utf8')
        except Exception as e:
            self.log.error("Sever connect fail: {0}".format(e))
        else:
            sql_base = 'SELECT a.business_date, b.manager, a.fund_name, a.asset_name from tmanager b, ' \
                       '(SELECT t.business_date, t.fund_id, max(t.fund_name) fund_name, t.asset_id, ' \
                       'max(t.asset_name) asset_name, t.operator_no from tentrusts t ' \
                       'WHERE t.operator_no = \'2\' and {0} ' \
                       'GROUP BY t.business_date, t.fund_id, t.asset_id, t.operator_no) a ' \
                       'WHERE b.asset_id = a.asset_id ' \
                       'ORDER BY a.business_date, b.manager, a.fund_name, a.asset_name'
            sql_detail = 'SELECT t.business_date, t.fund_name, t.asset_name, t.operator_no, t.report_code, ' \
                         't.entrust_time from tentrusts t ' \
                         'WHERE t.operator_no = \'2\' and {0} ' \
                         'ORDER BY t.business_date, t.fund_name, t.asset_name, t.report_code, t.entrust_time'
            if period != '':
                if len(period) == 2:
                    start_date = period[0]
                    end_date = period[1]
            else:
                start_date = dunhe_public.GetTradedate(daydiff=-5)
                end_date = dunhe_public.GetTradedate()
            sql_business_date = 't.business_date >= {0} and t.business_date <= {1}'.format(start_date, end_date)
            sql = sql_detail.format(sql_business_date)
            df = pd.DataFrame(pd.read_sql(sql, connection))
            df.to_excel(os.path.join(path, FILENAME_DETAIL))

            sql = sql_base.format(sql_business_date)
            df = pd.DataFrame(pd.read_sql(sql, connection))
            df.to_excel(os.path.join(path, FILENAME_SUM))


if __name__ == '__main__':
    log = dunhe_public.SetLog('Statistics')
    s1 = Statistics(log)
    filepath = 'G:\\data\\test'
    s1.count_not_use_oplus_product(path=filepath)
    receive_list = ['weiy@dunhefund.com', 'panhm@dunhefund.com', 'gaos@dunhefund.com']
    #receive_list = ['gaos@dunhefund.com']
    if 1:
        dunhe_public.SendingMailFromIT(Receive_list=receive_list, Subject='周度统计未使用Oplus交易的期货产品', Text='',
                                       Attachpath=os.path.join(filepath, FILENAME_SUM))
