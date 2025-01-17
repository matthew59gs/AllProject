#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 需要下载rarfile, python-dateutil, dbfread

import pymysql
import os
import logging
import datetime
import poplib
import email
from email import encoders
from email.header import Header
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import zipfile
import re
import rarfile
import sys
import dateutil.parser
import dbfread.dbf

# 公共函数
def SetLog(name):
	LOG_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	logger = logging.getLogger(__name__)
	logger.setLevel(level=logging.DEBUG)
	debuglog = logging.FileHandler(name + "_{0}_DEBUG.log".format(
		datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))
	debuglog.setLevel(logging.DEBUG)
	debuglog.setFormatter(LOG_FORMAT)
	logger.addHandler(debuglog)
	infolog = logging.FileHandler(name + "_{0}_INFO.log".format(
		datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))
	infolog.setLevel(logging.INFO)
	infolog.setFormatter(LOG_FORMAT)
	logger.addHandler(infolog)
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(LOG_FORMAT)
	logger.addHandler(console)
	return logger

#从字符串解析日期
def parse_date(_str, normal_diff = 0):
	match = re.findall(r"(\d{8})", _str)
	if match:
		for numbers in match:
			try:
				#解析的日期应该不会差太远，如果超过太远，则
				diff = datetime.datetime.now() - dateutil.parser.parse(numbers)
				if (normal_diff != 0) and ((diff.days > normal_diff) or (diff.days < -1 * normal_diff)):
					logger.debug("parse a date[{0}] but over diff[{1}]".format(numbers, normal_diff))
					continue
				return numbers
			except Exception as e:
				logger.debug("parse date[{0}] from [{1}] error {2}".format(numbers, _str, e))
	return ""

# Step 1 专用
def decode_str(s):
	#decode_header()返回一个list，因为像Cc、Bcc这样的字段可能包含多个邮件地址，所以解析出来的会有多个元素。
	#这里只取了第一个元素。如果是解析To字段，那么这种只分析第一个字段的做法是有问题的
	value, charset = decode_header(s)[0]
	if charset:
		value = value.decode(charset)
	return value

#解压文件
def unzipfile(filename):
	dir_path = os.path.dirname(filename)
	if filename.rfind(".zip") > 0:
		logger.info("Unzip file " + filename)
		zip_files = zipfile.ZipFile(filename)
		try:
			zip_files.extractall(dir_path, zip_files.namelist()) 
		except RuntimeError as e:
			try:
				logger.debug("Try password 888888 to unzip file " + filename)
				zip_files.extractall(dir_path, zip_files.namelist(), "888888".encode('utf-8')) 
			except RuntimeError as e:
				logger.error("Unzip " + filename + " failed. Bad pasword 888888! ")
				try:
					logger.debug("Try password dhdcl1hA to unzip file " + filename)
					zip_files.extractall(dir_path, zip_files.namelist(), "dhdcl1hA".encode('utf-8'))
				except RuntimeError as e:
					logger.error("Unzip " + filename + " failed. Bad pasword dhdcl1hA! ")
					raise e
		finally:
			zip_files.close()
	elif filename.rfind(".rar") > 0:
		'''
		cmd_command = "unrar.exe e " + filename + ' ' + dir_path
		logger.info('unrar command: ' + cmd_command)
		p = os.popen(cmd_command)
		logger.info('unrar result: ' + p.read())
		'''
		'''
		rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR"
		rarfile.PATH_SEP = '/'
		rar_files = rarfile.RarFile(filename)
		logger.info('Rarfile info {0}'.format(rar_files.namelist()))
		try:
			rar_files.extractall()
			rar_files.close()
		except Exception as e:
			logger.error("Unrar " + filename + " failed. {0}".format(e))
			raise e
		'''
		logger.info("escape unrar file " + filename)

#保存文件
def Save2Local(file, filename, date = ''):
	if not file:
		logger.error("To save file is null.")
		return

	if date == "":
		date = parse_date(filename, 100)
		if date == "":
			date = datetime.datetime.now().strftime("%Y%m%d")

	path = os.path.join(SAVE_PATH, date)
	if not os.path.exists(path):
		os.mkdir(path)

	logger.info("Save file[{0}] to {1}".format(filename, path))
	wfile = open(os.path.join(path, filename), "wb")
	wfile.write(file)
	wfile.close

	#zip文件解压
	if (filename.rfind(".zip") > 0) or ((filename.rfind(".rar") > 0)):
		unzipfile(os.path.join(path, filename))

#传入邮箱地址，传出对接结果，0-FALSE，1-TRUE
#data(id, address, servername, username, password, is_ssl, port)
#如果对接成功，同时传出server对象，如果失败，同时传出失败原因
def Connect2Mailserver(data):
	address = data[1]
	servername = data[2]
	username = data[3]
	password = data[4]
	is_ssl = data[5]
	port = data[6]
	logger.debug("Connect to {0}, address is {1}:{2}, username is {3}".format(servername, address, port, username))
	try:
		if is_ssl:
			logger.debug("Connect to server using SSL.")
			server = poplib.POP3_SSL(address, port)
		else:
			server = poplib.POP3(address, port)
		server.user(username)
		server.pass_(password)
		# stat()返回邮件数量和占用空间:
		logger.info('Messages: %s. Size: %s' % server.stat())
	except Exception as e:
		logger.error("Server connect fail: %s" % e)
		return (0, e)
	else:
		return (1, server)

#解析主题
def parse_subject(msg):
	value = msg.get('Subject', '')
	value = decode_str(value)
	return value

#解析发件人
def parse_from(msg):
	return email.utils.parseaddr(msg.get("From"))[1]

#解析附件
def parse_attachment(msg, rename = '', date = ''):
	i = 1
	for part in msg.walk():
		filename = part.get_filename()
		if filename:
			attachfilename = decode_str(filename)
			# h = email.header.Header(filename)
			# dh = email.header.decode_header(h)
			# attachfilename = dh[0][0]
			logger.info("Attachment name: {0}".format(attachfilename))
			if rename and (rename != ''):
				attachfilename = rename + '-' + str(i) + os.path.splitext(attachfilename)[1]
				i = i + 1
				logger.info("Rename attachment name: {0}".format(attachfilename))
			data = part.get_payload(decode=True)
			Save2Local(data, attachfilename, date)

#解析邮件，根据主题关键字，把附件保存到指定位置
#MatchTable: Subject, Sender, SubjectMatchType, AttachRename
def ParseMail(Server, MatchTable, start = 0):
	# list()返回所有邮件的编号:
	resp, mails, octets = Server.list()
	#logger.debug(resp)
	#logger.debug(mails)
	#logger.debug(octets)
	#默认取最后500封，如果有起始位置，就用起始位置
	if not start:
		start = len(mails) - MAX_MAIL_COUNT
	#start = 
	# 注意邮件的索引号从1开始
	for index in range(start, len(mails) + 1):
		logger.debug("Parsing mail[{0}]...".format(index))
		#解析这里有可能会出莫名其妙的错误，主要是从服务器可能断开了连接，要重新连上去继续读取
		try:
			#这里如果不扩展poplib._MAXLINE，可能会返回 line too long 错误，就是返回的lines长度超过了界限
			resp, lines, octets = Server.retr(index)
		except Exception as e:
			logger.error("Parse mail[{0}] error: {1}".format(index, e))
			return (1, index)

		# lines存储了邮件的原始文本的每一行,
		# 可以获得整个邮件的原始文本:
		try:
			msg_content = b'\r\n'.join(lines).decode('utf-8')
		except UnicodeDecodeError as e:
			try:
				msg_content = b'\r\n'.join(lines).decode('GBK')
			except UnicodeDecodeError as e:
				try:
					msg_content = b'\r\n'.join(lines).decode('GB2312')
				except UnicodeDecodeError as e:
					logger.debug("mail coding error " + e)
					raise e
			
		
		# 稍后解析出邮件:
		msg = Parser().parsestr(msg_content)
		subject = parse_subject(msg)
		_from = parse_from(msg)
		logger.debug("Parsing mail[{0}] subject[{1}] from[{2}]...".format(index, subject, _from))
		date = parse_date(subject, 100)
		for temple, sender, matchtype, attachrename in MatchTable:
			if temple.find("#YYYYMMDD#") > 0:
				temple = temple.replace("#YYYYMMD#", DEST_DIR_DATE)
			if (((matchtype == '1') and (subject.find(temple) == 0)) or \
			((matchtype == '2') and (subject.find(temple, 1) >= 0)) or \
			((matchtype == '3') and (subject.rfind(temple) >= 0))) and \
			(_from == sender):
				parse_attachment(msg, attachrename, date)
			else:
				logger.debug("mail[{0}] subject[{1}] unmatch[{2}][{3}].".format(index, subject, matchtype, temple))
	return (0, 0)

# Step 2 专用

'''持仓数据holddata：
日期
客户内部资金账
品种合约
买卖标志			B：买；S：卖
投机套保标志		S：投机；H：套保；	A：套利	中金所仅用“S：投机”	
持仓量
交易保证金
持仓盈亏(逐日盯
持仓盈亏(逐笔对
持仓均价
昨结算价
今结算价
交易编码
交易所统一标识	S：上海期货交易所；	Z：郑州商品交易所；	D：大连商品交易所；	J：中国金融期货交易所；	N：上海国际能源交易中心		
是否为交易会员	Y：是；N：否
币种
备兑标志
'''
def InsertSettlementData(data):
	try:
		connection = pymysql.connect(host='192.168.40.202', port=3306,\
			user='trader',password='123456',db='MailSaver',charset='utf8')
	except Exception as e:
		logger.error("Sever connect fail: {0}".format(e))
	else:
		cursor = connection.cursor()
		date = data[0]
		account = data[1]
		contract = data[2]
		direction = data[3]
		investtype = data[4]
		amount = data[5]
		hedging = data[6]
		profit_today = data[7]
		profit_float = data[8]
		avg_price = data[9]
		last_settle_price = data[10]
		settle_price = data[11]
		stockholder = data[12]
		exchange = data[13]
		trademember = data[14]
		currency = data[15]
		preparation = data[16]
		sql = "SELECT 1 FROM FutureHoldingDetail t WHERE t.date = \'{0}\' and t.account = \'{1}\' and t.contract = \'{2}\' and t.direction = \'{3}\' \
			and t.investtype = \'{4}\';".format(date, account, contract, direction, investtype)
		logger.debug("select sql: " + sql)
		try:
			cursor.execute(sql)
			result = cursor.fetchone()
			logger.debug("select sql result: {0}".format(result))
			if result is not None:
				sql = "DELETE FROM FutureHoldingDetail WHERE date = \'{0}\' and account = \'{1}\' and contract = \'{2}\' and direction = \'{3}\' \
					and investtype = \'{4}\';".format(date, account, contract, direction, investtype)
				logger.debug("delete sql: " + sql)
				cursor.execute(sql)
				connection.commit()
				logger.debug("Successfully Delete FutureHoldingDetail: date[{0}] account[{1}] contract[{2}] direction[{3}] investtype[{4}]".format(\
						date, account, contract, direction, investtype))
			sql = "insert into FutureHoldingDetail values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\'\
				, \'{11}\', \'{12}\', \'{13}\', \'{14}\', \'{15}\', \'{16}\');".format(date, account, contract, direction, investtype, amount, \
					hedging, profit_today, profit_float, avg_price, last_settle_price, settle_price, stockholder, exchange, trademember, currency, preparation)
			logger.debug("insert sql: " + sql)
			cursor.execute(sql)
			connection.commit()
			logger.debug("Successfully insert FutureHoldingDetail: date[{0}] account[{1}] contract[{2}] direction[{3}] investtype[{4}]".format(\
						date, account, contract, direction, investtype))
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))

'''资金数据：cusfund
日期
客户内部资金账户
资金权益总额
可用资金
需追加保证金
风险度
上日结存（逐日盯市）
上日结存（逐笔对冲）
当日结存（逐日盯市）
当日结存（逐笔对冲）
当日总盈亏（逐日盯市）
当日总盈亏（逐笔对冲）
浮动盈亏（逐笔对冲）
非货币充抵金额
是否为交易会员
币种
实有人民币资金
货币充抵金额
其它货币质出金额
货币质押保证金占用
当日总权利金
冻结资金
'''
def InsertCapitalData(data):
	try:
		connection = pymysql.connect(host='192.168.40.202', port=3306,\
			user='trader',password='123456',db='MailSaver',charset='utf8')
	except Exception as e:
		logger.error("Sever connect fail: {0}".format(e))
	else:
		cursor = connection.cursor()
		date = data[0]
		account = data[1]
		balance_total = data[2]
		available = data[3]
		added_deposit = data[4]
		risk = data[5]
		last_balance_day = data[6]
		last_balance_float = data[7]
		balance_day = data[8]
		balance_float = data[9]
		oneday_profit_day = data[10]
		oneday_profit_float = data[11]
		profit_float = data[12]
		compensate = data[13]
		trademember = data[14]
		currency = data[15]
		c1 = data[16]
		c2 = data[17]
		c3 = data[18]
		c4 = data[19]
		c5 = data[20].replace('\n', '')
		sql = "SELECT 1 FROM FutureCapitalDetail t WHERE t.date = \'{0}\' and t.account = \'{1}\';".format(date, account)
		logger.debug("select sql: " + sql)
		try:
			cursor.execute(sql)
			result = cursor.fetchone()
			logger.debug("select sql result: {0}".format(result))
			if result is not None:
				sql = "DELETE FROM FutureCapitalDetail WHERE date = \'{0}\' and account = \'{1}\';".format(date, account)
				logger.debug("delete sql: " + sql)
				cursor.execute(sql)
				connection.commit()
				logger.debug("Successfully Delete FutureCapitalDetail: date[{0}] account[{1}]".format(date, account))
			sql = "insert into FutureCapitalDetail values (\'{0}\', \'{1}\', {2}, {3}, {4}, {5}, \
				{6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, \'{14}\', \'{15}\', \
				{16}, {17}, {18}, {19}, {20});".format(date, account, balance_total, available, added_deposit, risk, \
				last_balance_day, last_balance_float, balance_day, balance_float, oneday_profit_day, oneday_profit_float, profit_float, compensate, trademember, currency, \
				c1, c2, c3, c4, c5)
			logger.debug("insert sql: " + sql)
			cursor.execute(sql)
			connection.commit()
			logger.debug("Successfully insert FutureCapitalDetail: date[{0}] account[{1}]".format(date, account))
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))

def GetDataFromFile(path, account_data):
	for account, filename, matchtype, filetype in account_data:
		if matchtype == 'R':
			filename = filename.replace('#ACCOUNT#', account).replace('#YYYYMMDD#', DEST_DIR_DATE)
		#logger.debug("GetDataFromFile path[{0}] compare with filename[{1}]".format(os.path.basename(path), filename))
		if os.path.basename(path) == filename:
			logger.info('Get settle file[{0}]'.format(filename))
			if filetype == 'Settlement':
				with open(path, 'r') as file:
					for line in file.readlines(): 
						data = line.split('@')
						logger.debug("Settlement File[{0}] get data: {1}".format(filename, data))
						InsertSettlementData(data)
			elif filetype == 'Capital':
				with open(path, 'r') as file:
					for line in file.readlines():
						data = line.split('@')
						logger.debug("Capital File[{0}] get data: {1}".format(filename, data))
						InsertCapitalData(data)


def GetDataFromDir(path, account_data):
	file_list = os.listdir(path)
	for file_path in file_list:
		a_path = os.path.join(path, file_path)
		if os.path.isdir(a_path):
			GetDataFromDir(a_path, account_data)
		else:
			GetDataFromFile(a_path, account_data)

# 主变量
#日志
logger = SetLog('FutureSettlementSave')
# 文件保存位置
SAVE_PATH = "D:\\data\\FutureSettlement"
# 读取哪天的结算文件
DEST_DIR_DATE = "20181008"
# 跳过下载邮件 0-不跳过 1-跳过
ESCAPE_DOWNLOADING = 1
# 分析下载的邮件数量
MAX_MAIL_COUNT = 300
# 手动解压缩标志
MANUAL = 0

#Step 1 解析邮件，把结算文件保存下来
if not ESCAPE_DOWNLOADING:
	poplib._MAXLINE=20480
	serverdata = ()
	mailsubjectdata = ()
	try:
		#数据库连接
		connection = pymysql.connect(host='192.168.40.202', port=3306,\
			user='trader',password='123456',db='MailSaver',charset='utf8')
	except Exception as e:
		logger.error("Sever connect fail: {0}".format(e))
	else:
		cursor = connection.cursor()
		sql_server = "SELECT ts.id, ts.Address, ts.ServerName, ts.Username, ts.`Password`, ts.Use_SSL, ts.port from ServerInfo ts \
			WHERE ServerName = \'Settlement\' AND type = \'POP\';"
		sql_mailsubject = "SELECT t.`Subject`, t.Sender, t.SubjectMatchType, t.AttachRename FROM FutureSettlementMail t;";
		try:
			#对接邮件服务器解析邮件
			logger.debug("select sql:" + sql_server)
			cursor.execute(sql_server)
			serverdata = cursor.fetchall()
			logger.debug("Get mail server info:%s" % serverdata)
			#先把主题的匹配内容，匹配规则取出来
			logger.debug("select sql:" + sql_mailsubject)
			cursor.execute(sql_mailsubject)
			mailsubjectdata = cursor.fetchall()
			logger.debug("Match table: {0}".format(mailsubjectdata))
			#关闭数据库
			cursor.close()
			connection.close()
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))
			raise e
	if serverdata:
		serverinfo = serverdata[0]
		logger.debug("Get one mail server info: {0}".format(serverinfo))

		ConnectResult = Connect2Mailserver(serverinfo)
		if not ConnectResult[0]:
			logger.error("Connect to server fail: %s" % ConnectResult[1])
		else:
			try:
				server = ConnectResult[1]
				#如果解析出了问题，会返回1，这里需要重试
				parseResult = ParseMail(server, mailsubjectdata)
				while parseResult[0]:
					index = parseResult[1]
					#server.quit()
					server = Connect2Mailserver(serverinfo)[1]
					parseResult = ParseMail(server, mailsubjectdata, index)
			except Exception as e:
				logger.error("Connect/parse mail error:{0}".format(e))
				raise e
			finally:
				server.quit()
			logger.info("Save settlement file over!")
	else:
		logger.info("Get mail server info error, no server!")

# 手工解压
if MANUAL:
	sys.exit()

#Step 2 进入文件夹，把DBF，TXT，读入到数据库中
try:
	#数据库连接
	connection = pymysql.connect(host='192.168.40.202', port=3306,\
			user='trader',password='123456',db='MailSaver',charset='utf8')
except Exception as e:
	logger.error("Sever connect fail: {0}".format(e))
else:
	cursor = connection.cursor()
	sql = "SELECT t.Account, t.Filename, t.Matchtype, t.Filetype FROM FutureSettlementFile t;"
	logger.debug("select sql:" + sql)
	try:
		cursor.execute(sql)
		account_data = cursor.fetchall()
		logger.debug("select sql result: {0}".format(account_data))
		DES_DIR = os.path.join(SAVE_PATH, DEST_DIR_DATE)
		file_list = os.listdir(DES_DIR)
		for file_path in file_list:
			a_path = os.path.join(DES_DIR, file_path)
			if os.path.isdir(a_path):
				GetDataFromDir(a_path, account_data)
			else:
				GetDataFromFile(a_path, account_data)
	except Exception as e:
		logger.error("Sql execute error: {0}".format(e))
		raise e
