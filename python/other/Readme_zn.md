# 临时性功能


---

## 文件列表

 - hisnetvalue-ForOplus.py  从数据中心导出净资产，单位净值到Excel
 - Rename.py    根据数据库设置批量改名字
 - UserAvgAsset.py  测试性代码
 - weekly_not_use_oplus_trade.py    每周没有使用Oplus交易的产品列表
 - xml_import.py  文件导出成Excel

##功能说明
#### weekly_not_use_oplus_trade
统计从统计日算起，往前推5天的，所有的Oplus的委托记录里面，操作员是2-补委托操作员的委托
输出的文件有两个，Statistics_sum.xlsx 和 Statistics_detail.xlsx
其中sum文件有基金经理的名字，而detail是委托的明细数据
sun文件发送给相关人员
修改导出路径，邮件发送人员，都要直接修改代码

