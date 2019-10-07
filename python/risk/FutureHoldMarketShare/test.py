#!/usr/bin/env python

import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import pandas as pd
from openpyxl import load_workbook

## 一个Sheet的数据，拆分成多个Sheet
writer = pd.ExcelWriter('all.xlsx', engine='openpyxl')
book = load_workbook(writer.path)
writer.book = book
df_ori = pd.read_excel('ratio-his.xlsx')
df = df_ori.copy()
for name, group in df.groupby(df['fund_name']):
    group.to_excel(excel_writer=writer,sheet_name=name,index=False,header=True)
writer.save()
writer.close()
