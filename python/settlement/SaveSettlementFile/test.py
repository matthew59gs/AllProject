# -*- coding:utf-8 -*-

import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import pandas as pd
import numpy as np

logger = dunhe_public.SetLog('TEST')

list1 = [[1,2], [3,4]]
list2 = [[5,6], [7.8]]
list3 = []
list3.append(list1)
list3 = list3 + list2
print(list3)

#df = pd.DataFrame(pd.read_excel('G:\\data\\SGD272\\SGD272_3\\敦和永好1号-客户对账单-2800014273_普通对账单_20190517.xlsx'))
#for index, row in df.iterrows():
#    if not pd.isnull(row[0]):
#        print(row[0])

#dict1 = {1:'aaaa', 2:'bbbb', 3:'cccc'}
#for key in dict1.keys():
#    dict1[str(key)] = dict1.pop(key)
#print(dict1)

# str1 = '国泰君安证券资产托管估值表发送：SGD272_敦和永好1号私募证券投资基金20190416估值表'
# str2 = '国泰君安证券资产托管估值表发送：SGD272_敦和永好1号私募证券投资基金'
#
# (result, server) = dunhe_public_tmp.ConnectSettmentMailServer()
# try:
#     if result:
#         SubjectMatchTable = [['SGD272-3', '敦和永好1号-客户对账单-2800014273_', 1, 'D:\\data\\SGD272', 2],
#                              ['SGD272-1', '国泰君安证券资产托管估值表发送：SGD272_敦和永好1号私募证券投资基金', 1, 'D:\\data\\SGD272', 2],
#                              ['SGD272-4', '敦和永好1号 的交易所格式数据', 2, 'D:\\data\\SGD272', 2]]
#         save_list = dunhe_public_tmp.ParseMailSaveAttach(server, SubjectMatchTable, 147139)
#         logger.info(save_list)
# finally:
#     server.quit()