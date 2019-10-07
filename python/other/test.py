# -*- condig: utf-8 -*-
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public
import datetime
import xml.etree.ElementTree
import pandas as pd

def GetNodeData(father_node, child_node_name):
    result_list = []
    for node in father_node.iter(child_node_name):
        node_children = node.getchildren()
        if node_children:
            for node_child in node_children:
                result_list.append(node_child.text)
                #print(node_child.tag, node_child.text)
        else:
            result_list.append(node.text)
            #print(node.tag, node.text)
    if len(result_list) == 0:
        return None
    else:
        return result_list

pd.set_option('display.width', 1000)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
df = pd.DataFrame([])

with open('G:\\data\\wujiang.xml','r',encoding="utf-8") as file:
    strXml = file.read()
    root = xml.etree.ElementTree.XML(strXml)
    row = -1
    for node_li in root.iter('li'):
        list_row = []

        list_div = GetNodeData(node_li, 'div')
        if list_div:
            list_row = list_row + list_div
        list_span = GetNodeData(node_li, 'span')
        if list_span:
            list_row = list_row + list_span
        list_en = GetNodeData(node_li, 'em')
        if list_en:
            list_row = list_row + list_en
        list_i = GetNodeData(node_li, 'i')
        if list_i:
            list_row = list_row + list_i

        if row == -1:
            for col_name in list_row:
                df[col_name] = ''
        else:
            df.loc[row] = list_row
        row = row + 1
df.to_excel('G:\\data\\wujiang.xlsx')

#dunhe_public.WriteMultiData2Excel('G:\\data\\TEST.xlsx', ('1', '2'), ((('A', 1), ('B', 2)), (('C', 3), ('D', 4))))

#data = dunhe_public.ReadExcel2List('G:\\data\\Oplus产品信息.xls')
#print('{0}'.format(data))

#print(dunhe_public.GetTradedate(datetime.datetime.now().strftime("%Y%m%d"), -1))

#print(dunhe_public.GetTradedate(datetime.datetime.now().strftime("%Y%m%d"), -1))



'''
list1 = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
for d1, d2, d3 in list1:
	print(d1)
	d1 = 10
print(list1)

for i in range(len(list1)):
	print(list1[i][0])
	list1[i][0] = 10 + list1[i][0]
print(list1)
'''