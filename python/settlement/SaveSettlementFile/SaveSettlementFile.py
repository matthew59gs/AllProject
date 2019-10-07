# -*- coding:utf-8 -*-

import pymysql
import pandas as pd
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public

class SettlementFileSaver:
    # dictFilePath结构：{1:'Path1', 2:'Path2'}
    #   1-估值表；2-预估值；3-证券结算文件；4-期货结算文件；5-场外结算文件；6-期权结算文件
    def __init__(self, logger, dictFilePath = {}):
        self.logger = logger
        self.dictFilePath = dictFilePath

    def SaveFile(self, product_list = {}, max_mail_count = 500, tradedate = 0):
        try:
            conn = pymysql.connect(host='192.168.40.203', port=3306,
                                   user='risk', password='risk', db='risk', charset='utf8')
        except Exception as e:
            self.logger.error("Sever[{0}] connect fail: {0}".format('192.168.40.202:risk', e))
        else:
            # 1 数据库里面的匹配规则取出来
            dicFilePathstr = map(lambda x:str(x), self.dictFilePath.keys())
            sql_filetype = ','.join(dicFilePathstr)
            if sql_filetype == '':
                return None
            if len(product_list) > 0:
                products = '\',\''.join(product_list)
                sql = 'SELECT fund_code, `subject`, subject_match_type, file_type FROM tmail_match t WHERE 1=1 ' \
                      'and t.file_type in ({0}) and t.fund_code in (\'{1}\')'.format(sql_filetype, products)
            else:
                sql = 'SELECT fund_code, `subject`, subject_match_type, file_type FROM tmail_match t WHERE 1=1 ' \
                      'and t.file_type in ({0})'.format(sql_filetype)
            self.logger.debug('Select sql: ' + sql)
            df = pd.DataFrame(pd.read_sql(sql, conn))

            # 2 匹配规则和路径结合
            SubjectMatchTable = df.copy()
            df['Key'] = df['fund_code'] + '_' + df['file_type'].map(str)
            SubjectMatchTable['Key'] = SubjectMatchTable['fund_code'] + '_' + SubjectMatchTable['file_type'].map(str)
            SubjectMatchTable['AttachSaveMode'] = SubjectMatchTable['file_type'].apply(lambda x: 2 if x==3 else(2 if x==4 else 1))
            SubjectMatchTable['Path'] = SubjectMatchTable['file_type']
            SubjectMatchTable['Path'].replace(self.dictFilePath, inplace=True)
            SubjectMatchTable.rename(columns={'subject':'Subject', 'subject_match_type':'SubjectMatchMode'}, inplace=True)
            self.logger.info('Subject match table:\n{0}'.format(SubjectMatchTable))

            # 3 取出邮件，配对匹配
            (result, server) = dunhe_public.ConnectSettmentMailServer()
            if not result:
                self.logger.error('Connect settlement server fail!')
                return
            # 这里返回的savelist，['Key', '']
            savelist = []
            iMaxRetry = 2
            result = dunhe_public.ParseMailSaveAttach(Server=server, SubjectMatchTable=SubjectMatchTable, MaxMailCount=max_mail_count)
            while result[0] != 0 and iMaxRetry > 0:
                savelist = savelist + result[1]
                start = result[2]
                result = dunhe_public.ParseMailSaveAttach(Server=server, Start=start,
                                                          SubjectMatchTable=SubjectMatchTable,
                                                          MaxMailCount=max_mail_count)
                iMaxRetry = iMaxRetry - 1
            savelist = savelist + result[1]
            savetable = pd.DataFrame(savelist)
            savetable.columns = ['Key', 'Savedate']
            savetable.to_excel('savelist.xlsx')
            self.logger.debug('Settlement file save result:\n{0}'.format(savelist))

            # 4 配对结果和产品记录结合，形成配对结果
            # sql = 'SELECT fund_code, fund_name from tfund;'
            # fundinfo = pd.DataFrame(pd.read_sql(sql, conn))
            # df1 = pd.merge(SubjectMatchTable, savelist, on=['Key'], how='outer')
            # savecheck = pd.merge(df1, fundinfo, on=['fund_code'], how='outer')
            # savecheck['CheckResult'] = savecheck['Savedate'].apply(lambda x: True if x == tradedate else False)
            #
            # for index, row in savecheck.iterrows():
            #     checkresult = row['CheckResult']
            #     fundname = row['fund_name']
            #     savedate = row['Savedate']
            #     filetype = row['filetype']
            #     dicfiletype = {1:'nettable', 2:'prenettable', 3:'stocksettlefile', 4:'futuresettlefile'}
            #     if checkresult:
            #         self.logger.info('{0} save {1} successfully'.format(fundname, dicfiletype[filetype]))
            #     else:
            #         self.logger.info('{0} save {1} fail, target date {2}, save date {3}'.format(fundname, dicfiletype[filetype], tradedate, savedate))

