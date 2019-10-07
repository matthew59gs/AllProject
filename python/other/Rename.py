#!/usr/bin/env python
# -*- coding:utf-8 -*-
#根据匹配规则，将固定路径下的文件改名
# 1、从数据库取出邮件服务器位置
# 2、从数据库取出产品代码和修改规则
# 3、在指定目录下，产品代码找到文件，根据规则进行修改
# 4、修改的文件进入rename目录，源文件保留

import pymysql
import os
import shutil
import logging
import datetime
import re
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

def single_rename(filename, rule, code, date = ''):
    realname = os.path.basename(filename)
    #原路径下加一个rename文件夹，改名后的都放进去
    savepath = os.path.join(os.path.dirname(filename), "rename")
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    if date == "":
        match = re.search(r"(\d{8})", realname)
        if match:
            date = match.group(0)
        else:
            date = datetime.datetime.now().strftime("%Y%m%d")

    dest_name = rule
    if rule.find("#CODE") >= 0:
        dest_name = dest_name.replace("#CODE", code)
    if rule.find("#DATE") >= 0:
        dest_name = dest_name.replace("#DATE", date)
    suffix = os.path.splitext(filename)[1]
    dest_file = os.path.join(savepath, dest_name) + suffix
    logger.info("Copy " + filename + " to " + dest_file)
    shutil.copyfile(filename, dest_file)

def batch_rename(rule, dest_dir):
    count = 0
    file_list = os.listdir(dest_dir)
    for i in range(0, len(file_list)):
        path = os.path.join(dest_dir, file_list[i])
        if os.path.isfile(path):
            filename = file_list[i]
            for single_rule in rule:
                fund_name = single_rule[0]
                code = single_rule[1]
                match_type = single_rule[2]
                rename_rule = single_rule[3]
                if ((match_type == '1') and (filename.find(code) >= 0)) or \
                ((match_type == '2') and (filename.find(fund_name) >= 0)):
                    logger.debug("File " + path + " match " + rename_rule + " with code " + code)
                    single_rename(path, rename_rule, code)
                    count += 1
    return count

def NetTableRename(I_date, I_dir, I_tabletype):
    if I_tabletype == "PreNetTable" :
        sql_code = "SELECT tf.FundName, tf.FundCode, tf.PreNetRenameMatchType, tf.PreNetRename FROM FundInfo_ALL tf WHERE 1 = 1 AND tf.Valid = \'1\';";
    elif  I_tabletype == "NetTable" :
        sql_code = "SELECT tf.FundName, tf.FundCode, tf.NetRenameMatchType, tf.NetRename FROM FundInfo_ALL tf WHERE 1 = 1 AND tf.Valid = \'1\';";
    else:
        return
    
    dest_date = I_date
    if dest_date == "":
        dir_list = os.listdir(I_dir)
        date = 0
        for i in range(0, len(dir_list)):
            if not os.path.isfile(os.path.join(I_dir, dir_list[i])):
                if dir_list[i].isdigit():
                    if int(dir_list[i]) > date:
                        date = int(dir_list[i])
        if date > 0:
            dest_date = str(date)
    DEST_DIR = os.path.join(I_dir, dest_date)

    #手工设置改名规则
    '''
    code_rename = (('八卦田4号','SM9264','1','GZ#CODE_#DATE'),\
        ('玉皇山1号','S23346','1','GZ#CODE_#DATE'),\
        ('多策略1号A基金','S20238','1','GZ#CODE_#DATE'),\
        ('玉皇山4号','SE5146','1','GZ#CODE_#DATE'),\
        ('玉皇山2号','SE5143','1','GZ#CODE_#DATE'),\
        ('八卦田1号','S23345','1','GZ#CODE_#DATE'),\
        ('慈善基金','S23344','1','GZ#CODE_#DATE'),\
        ('玉皇山3号','SE5144','1','GZ#CODE_#DATE'),\
        ('云栖3号','SE2304','1','GZ#CODE_#DATE'),\
        ('云栖1号','SE2302','1','GZ#CODE_#DATE'),\
        ('云栖2号','SE2303','1','GZ#CODE_#DATE'),\
        ('玉皇山5号','SE5196','1','GZ#CODE_#DATE'),\
        ('龙井1号','SW4950','1','GZ#CODE_#DATE'),\
        ('富春价差','SW6881','2','GZ#CODE_#DATE'),\
        ('八卦田积极A','ST6703','1','GZ#CODE_#DATE'),\
        ('桂雨1号','ST9820','1','GZ#CODE_#DATE'),\
        ('云栖4号','SE5116','1','GZ#CODE_#DATE'),\
        ('六和2号','SH6651','1','GZ#CODE_#DATE'),\
        ('西湖1号','SW9390','1','GZ#CODE_#DATE'),\
        ('白塔1号','SX1112','1','GZ#CODE_#DATE'),\
        ('峰云1号','SX1114','1','GZ#CODE_#DATE'),\
        ('之江1号','SX1116','1','GZ#CODE_#DATE'),\
        ('起航1号','SX1115','1','GZ#CODE_#DATE'),\
        ('CTA1号','SY2788','1','GZ#CODE_#DATE'),\
        ('八卦田积极B','X4617S5','1','GZ#CODE_#DATE'),\
        ('龙井2号','X4576S5','1','GZ#CODE_#DATE'),\
        ('山南1号','SX6170','1','GZ#CODE_#DATE'),\
        ('巨子1号','SX5222','1','GZ#CODE_#DATE'),\
        ('云栖指数增强','SY8486','1','GZ#CODE_#DATE'),\
        ('凤起1号','SCJ996','1','GZ#CODE_#DATE'),\
        ('灵隐1号','X5091S5','1','GZ#CODE_#DATE'),\
        ('之江2号','SY3864','1','GZ#CODE_#DATE'),\
        ('宏观对冲1号','X5107S5','1','GZ#CODE_#DATE'),\
        ('九溪1号','SCJ994','1','GZ#CODE_#DATE'),\
        ('涌金1号','SCM779','1','GZ#CODE_#DATE'),\
        ('平湖1号','X5396S5','1','GZ#CODE_#DATE'),\
        ('复兴1号','X5426S5','1','GZ#CODE_#DATE'))
    '''

    try:
        connection = pymysql.connect(host='192.168.40.202', port=3306,\
            user='trader',password='123456',db='MailSaver',charset='utf8')
    except Exception as e:
        logger.error("Sever connect fail: {0}".format(e))
    else:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_code)
            code_rename = cursor.fetchall()
            logger.debug("Get code rename rule:{0}".format(code_rename))
            #关闭数据库
            cursor.close()
            connection.close()
        except Exception as e:
            logger.error("Sql execute error: {0}".format(e))

    count = batch_rename(code_rename, DEST_DIR)
    logger.info("Rename over! Batch rename {0} files.".format(count))

#日志
NET_TABLE_TYPE = "NetTable"
#NET_TABLE_TYPE = "PreNetTable"
logger = dunhe_public.SetLog("Rename_" + NET_TABLE_TYPE)
DEST_DIR_ROOT = "G:\\data\\NetTable"
DEST_DIR_DATE = ""

if len(sys.argv) > 1:
    NET_TABLE_TYPE = sys.argv[1]
    if len(sys.argv) > 2:
        DEST_DIR_ROOT = sys.argv[2]
        if len(sys.argv) > 3:
            DEST_DIR_DATE = sys.argv[3]

NetTableRename(DEST_DIR_DATE, DEST_DIR_ROOT, NET_TABLE_TYPE)
