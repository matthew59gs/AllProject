#!/usr/bin/env python
# -*- coding:utf-8 -*-

import HoldingShareFromMarket3
import datetime
import os
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

if __name__ == "__main__":
    '''
    sys.argv[1] SendMail=1, Don'tSendMail=0
    sys.argv[2] FileSavePath
    sys.argv[3] Date, if Null, then today
    '''
    # 日志
    # 读取哪天的行情
    if len(sys.argv) >= 3:
        logger = dunhe_public.SetLog('HoldingShareFromMarket')
        SENDING_MAIL = sys.argv[1]
        SAVE_PATH = sys.argv[2]
        if len(sys.argv) == 4:
            HQ_DATE_OPLUS = sys.argv[3]
        else:
            HQ_DATE_OPLUS = datetime.datetime.now().strftime("%Y%m%d")

        # 文件保存位置
        SAVE_FILENAME = HQ_DATE_OPLUS + '期货持仓占比概况.xlsx'
        RECIEVE_LIST = ['gaos@dunhefund.com', 'tanghj@dunhefund.com', 'panhm@dunhefund.com']
        #RECIEVE_LIST = ['gaos@dunhefund.com']
        SUBJECT = HQ_DATE_OPLUS+'期货持仓占比定时发送'

        datamerger = HoldingShareFromMarket3.DataMerge(logger,
                                                       HoldingShareFromMarket3.BasicHoldingReceiver(logger).GetHoldingData(HQ_DATE_OPLUS),
                                                       HoldingShareFromMarket3.HQReceiver(logger).GetMarketData(HQ_DATE_OPLUS))
        companydata = datamerger.MergerHqDataAndHoldingData(HoldingShareFromMarket3.DemensionType.Company)
        futruemanagerdata = datamerger.MergerHqDataAndHoldingData(HoldingShareFromMarket3.DemensionType.FutureManager)
        datamerger.OutputExcelDataWithDataframe(os.path.join(SAVE_PATH, SAVE_FILENAME), ('company', 'futruemanager'), (companydata, futruemanagerdata))
        if SENDING_MAIL == '1':
            dunhe_public.SendingMailFromIT(Receive_list=RECIEVE_LIST, Subject=SUBJECT, Attachpath=os.path.join(SAVE_PATH, SAVE_FILENAME))