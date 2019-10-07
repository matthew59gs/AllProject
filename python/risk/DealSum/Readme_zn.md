# DealSum

根据输入条件，将成交汇总，计算某一段时间的成交均价。
例如输入条件为
date=[20190301,20190320] contract=[I1909] fundname=[玉皇山1号,八卦田1号] entrust_direction=[买入开仓,卖出平仓] path=G:\data\test
意思是，计算20190301到20190320之间，I1909合约，玉皇山1号和八卦田1号的买入开仓,卖出平仓的成交，按照5分钟的时间间隔做汇总，计算成交均价，结果导出为Excel，到G:\data\test目录
导出的Excel的格式抬头为：
sort_num：排列序号，无实际意义
business_date：交易日
deal_time_min：一批成交的最早成交时间
deal_time_max：一批成交的最晚成交时间
contract：合约
fund_name：产品名称
deal_amount：一批成交的成交数量
deal_balance：一批成交的成交金额
entrust_direction：委托方向
avg_price：一批成交的成交均价

## 文件列表 ##

 - DealSum  主文件目录
- dealsum.py    主功能文件
- main.py   主调用文件
- main-model.bat    调用入口，含入参
- readme.md 说明文件
