# -*- coding:utf-8 -*-

import datetime
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import SaveSettlementFile
import ImportSettlementFile

if __name__ == '__main__':
    logger = dunhe_public.SetLog('SaveSettlementFile')
    dictfilepath = {4: 'G:\\data\\SE5146'}
    product_list = {'SE5146'}
    tradedate = dunhe_public.GetTradedate()
    if tradedate != datetime.datetime.now().strftime("%Y%m%d"):
        tradedate = dunhe_public.GetTradedate(-1)
    mailsaver = SaveSettlementFile.SettlementFileSaver(logger, dictFilePath=dictfilepath)
    mailsaver.SaveFile(max_mail_count=7000, product_list=product_list, tradedate=dunhe_public.GetTradedate())


    #logger = dunhe_public.SetLog('ImportSettlementFile')
    #import1 = ImportSettlementFile(logger)
    #import1.set_product_path()
    #import1.import_file()