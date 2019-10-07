cd C:\Users\gaos\Documents\project\Settlement\python\SaveSettlementFile
rem SaveSettlementFile.py 参数：往前N天交易日，1-估值表位置，2-预估值位置，3-证券结算文件位置，4-期货结算文件位置，5-期权结算文件位置
rem 估值表一般是T-2
python SaveSettlementFile.py -2 1:'G:\\data\\NetTable'
rem 证券结算文件都是T-1，期货一般是T日日终，这里放在一起
python SaveSettlementFile.py -1 3:'G:\\data\\SGD272' 4:'G:\\data\\SGD272' 5:'G:\\data\\SGD272'