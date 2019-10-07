#coding = UTF-8
import time
import os
import shutil

'''
检查文件是否在对应目录下，如果存在，就新建一个日期的目录准备拷贝用
并把文件加入文件队列中，准备拷贝
'''
def checkfile(filename,  dirname,  filelist):
    if len(filename) == 0:
        return
    if len(dirname) == 0:
        return

    if os.path.isfile(os.path.join(dirname, filename)):
        if not os.path.exists(os.path.join(dirname, daytime)):
            os.mkdir(os.path.join(dirname, daytime))
    filelist.append(filename)   

def movedirfile(srcdir, destdir):
    #源目录不存在，结束
    if not os.path.exists(srcdir):
        return

    filelist = os.listdir(srcdir)
    # 注意删除只能倒叙
    for file in filelist[::-1]:
        if os.path.isdir(os.path.join(srcdir, file)):
            filelist.remove(file)

    # 建立文件夹
    if not os.path.exists(os.path.join(destdir, daytime)):
        os.mkdir(os.path.join(destdir, daytime))

    for file in filelist:
        targetfile = daytime + '_' + file
        if os.path.isfile(os.path.join(srcdir, file)):
            shutil.move(os.path.join(srcdir, file), \
                os.path.join(destdir, daytime, targetfile))

'''
迅投PB
一般来说有持仓资金和成交3种文件，然后分境内，沪港通、深港通3种，所以一般9个文件
每个文件都是自己命名的，所以不区分文件名，直接全部拷贝
'''
def XTCopy(dirname):
    movedirfile(os.path.join(dirname, "hold"), dirname)
    movedirfile(os.path.join(dirname, "hk-hold"), dirname)
    movedirfile(os.path.join(dirname, "hksh-hold"), dirname) 
    movedirfile(os.path.join(dirname, "hksz-hold"), dirname) 
    movedirfile(os.path.join(dirname, "capital"), dirname)
    movedirfile(os.path.join(dirname, "deal"), dirname) 
    movedirfile(os.path.join(dirname, "hk-deal"), dirname)
    movedirfile(os.path.join(dirname, "hksh-deal"), dirname) 
    movedirfile(os.path.join(dirname, "hksz-deal"), dirname) 

'''
恒生PB
需要备份4个文件
委托Tentrusts_20180313
成交Trealdeal_20180313
资金ZJ_S6LZYXYEZZ9395WDSNMW_20180313
持仓CC_S6LZYXYEZZ9395WDSNMW_20180313
委托和成交，后面是日期
资金和持仓，中间有一段每个券商PB的识别号
'''
def HSbackup(dirname, localstr):
    c_entrust = "Tentrusts_D1.log"
    c_realdeal = "Trealdeal_D1.log"
    c_capital = "ZJ_S1_D1.log"
    c_hold = "CC_S1_D1.log"
    if dirname[-1] != os.sep:
        dirname = dirname + os.sep
    filelist = []
    checkfile(c_entrust.replace("D1", daytime), dirname,  filelist)
    checkfile(c_realdeal.replace("D1", daytime),  dirname,  filelist)
    checkfile(c_capital.replace("S1", localstr).replace("D1", daytime), dirname,  filelist)
    checkfile(c_hold.replace("S1", localstr).replace("D1", daytime), dirname,  filelist)
    for file in filelist:
        if os.path.isfile(os.path.join(dirname, file)):
            shutil.copyfile(os.path.join(dirname, file), dirname + daytime + os.sep + file)

'''
DBF文件找对应日期的，然后放入对应的日期文件夹下
'''
def MoveDBFFile(path):
    if not os.path.exists(path):
        return

    filelist = os.listdir(path)
    for file in filelist:
        #能找到，就直接往里面拷贝
        if os.path.isdir(os.path.join(path, file)) and os.path.basename(file) == daytime:
            for file in DBFFile:
                if os.path.exists(os.path.join(path, file.replace(DATE_PREFIX, daytime))):
                    shutil.move(os.path.join(path, file.replace(DATE_PREFIX, daytime)), os.path.join(path, daytime))
            return

    #找不到，就新建目录拷贝
    os.mkdir(os.path.join(path, daytime))
    for file in DBFFile:
        if os.path.exists(os.path.join(path, file.replace(DATE_PREFIX, daytime))):
            shutil.move(os.path.join(path, file.replace(DATE_PREFIX, daytime)), os.path.join(path, daytime))
    

if __name__ == '__main__':
    daytime = time.strftime('%Y%m%d')
    #daytime = '20180920'

    #恒生PB
    backupdirctory1 = "E:\\pbrc\\Logs"
    localstr = "N3U05NP8PKKEMYE1YTFM"
    HSbackup(backupdirctory1,  localstr)

    DATE_PREFIX = '#YYYYMMDD#'
    #保存DBF文件
    DBFFile = ("XHPT_CD#YYYYMMDD#.dbf", "XHPT_CJCX#YYYYMMDD#.dbf", "XHPT_WT#YYYYMMDD#.dbf", "XHPT_WTCX#YYYYMMDD#.dbf")
    DBFpath = "E:\\DBF\\SWZQ-LY1"
    MoveDBFFile(DBFpath)
    #保存算法DBF文件
    DBFFile = ("XHPT_CJCX#YYYYMMDD#.dbf", "XHPT_CLKZ#YYYYMMDD#.dbf", "XHPT_CLWT#YYYYMMDD#.dbf", "XHPT_FACX#YYYYMMDD#.dbf", "XHPT_WTCX#YYYYMMDD#.dbf")
    DBFpath = "E:\\DBF\\SWZQ-LY1\\SF"
    MoveDBFFile(DBFpath)