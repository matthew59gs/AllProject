#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import os
import shutil
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

def CopyFileFromList(dirlist, filelist):
	if len(dirlist) == 0 or len(filelist) == 0:
		return

	daytime = time.strftime('%Y%m%d')
	for srcdir, destdir in dirlist:
		for filename in filelist:
			a_file = filename.replace(MACRO_DATE, daytime)
			if os.path.isfile(os.path.join(srcdir, a_file)):
				shutil.copy(os.path.join(srcdir, a_file), destdir)


DIR_LIST = [("E:\\CSC_PB_Client_Prod_20180324\\Logs", "E:\\output\\HSPB\\ZXJT"), \
		("E:\\财通证券恒生PB交易系统客户端\\PBRC\\Logs", "E:\\output\\HSPB\\CTZQ")]
COPY_FILE_LIST = ["Tentrusts_#YYYYMMDD#.log", "Trealdeal_#YYYYMMDD#.log"]

MACRO_DATE = "#YYYYMMDD#"
CopyFile(DIR_LIST, COPY_FILE_LIST)
MACRO_DATE = "#YYYYMMDD#"

CopyFileFromList(DIR_LIST, COPY_FILE_LIST)
