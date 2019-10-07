# -*- coding:utf-8 -*-

import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import dealsum

def getParaInfoList(para=''):
    if para == '':
        return
    if para.find('[') > 0 and para.find(']') > 0:
        str_list = para.split('=')[1][1:-1]
    else:
        str_list = para.split('=')[1]
    if len(str_list) > 0:
        a_list = []
        for a_str in str_list.split(','):
            a_list.append(a_str)
        return a_list
    else:
        return []

if __name__ == '__main__':
    logger = dunhe_public.SetLog('DealSum')
    if len(sys.argv) < 6:
        sys.exit()
    else:
        date_list = getParaInfoList(sys.argv[1])
        contract_list = getParaInfoList(sys.argv[2])
        fund_name_list = getParaInfoList(sys.argv[3])
        entrust_direction_list = getParaInfoList(sys.argv[4])
        path = getParaInfoList(sys.argv[5])[0]
        dealsum1 = dealsum.DealSum(logger)
        dealsum1.calc_deal(date_list=date_list, contract_list=contract_list, product_list=fund_name_list,
                           entrust_direction=entrust_direction_list, path=path)