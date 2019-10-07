#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 按照数据库的配置，从邮箱读取邮件，把附件放到对应的位置
# 1、从数据库取出邮件服务器位置
# 2、从数据库取出邮件主题和对应存放位置
# 3、从数据库取出邮件改名规则
# 4、对接邮件服务器，扫描邮件按照主推提取附件保存
# 5、附件有压缩的，解压

import pymysql
import os
import sys
import datetime
import poplib
import email
from email.parser import Parser
import re
sys.path.append("..\\..\\public\\python")
import dunhe_public

global logger
global MAX_MAIL_COUNT
global SAVE_PATH

#保存文件
def Save2Local(file, filename, date = ''):
	if not file:
		logger.error("To save file is null.")
		return

	if date == "":
		match = re.search(r"(\d{8})", filename)
		if match:
			date = match.group(0)
		else:
			date = datetime.datetime.now().strftime("%Y%m%d")

	path = os.path.join(SAVE_PATH, date)
	if not os.path.exists(path):
		os.mkdir(path)
	logger.info("Save file[{0}] to {1}".format(filename, path))
	wfile = open(os.path.join(path, filename), "wb")
	wfile.write(file)
	wfile.close

	#zip文件解压
	if filename.rfind(".zip") > 0:
		dunhe_public.unzipfile(filename=os.path.join(path, filename), passwordlist=["888888", "dhdcl1hA"])

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

def parse_attachment(msg, date = ''):
	for part in msg.walk():
		filename = part.get_filename()
		if filename:
			attachfilename = dunhe_public.decode_str(filename)
			# h = email.header.Header(filename)
			# dh = email.header.decode_header(h)
			# attachfilename = dh[0][0]
			logger.info("Attachment name: {0}".format(attachfilename))
			# if dh[0][1]:
			# 	attachfilename = attachfilename.decode(dh[0][1])
			# 	attachfilename = attachfilename.encode("utf-8")
			data = part.get_payload(decode=True)
			Save2Local(data, attachfilename, date)

#解析邮件，根据主题关键字，把附件保存到指定位置
def ParseMail(Server, MatchTable, start = 0):
	#可能邮件正文太长，需要扩大，默认是2048
	poplib._MAXLINE = 20480

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
				except Exception as e:
					logger.debug('decode mail fail mail id {0}, mail context: {1}'.format(index, lines))
					logger.info('skip mail[{0}]'.format(index))
					continue
		
		# 稍后解析出邮件:
		msg = Parser().parsestr(msg_content)
		subject = dunhe_public.parse_subject(msg)
		logger.debug("Parsing mail[{0}] subject[{1}]...".format(index, subject))
		match = re.search(r"(\d{8})", subject)
		if match:
			date = match.group(0)
		else:
			date = ""
		for i in range(0, len(MatchTable)):
			temple = MatchTable[i][1]
			matchtype = MatchTable[i][2]
			if dunhe_public.StringMatch(matchtype, temple, subject):
				MatchTable[i][3] = '1' #MatchResult
				if date:
					parse_attachment(msg, date)
				else:
					parse_attachment(msg)
			else:
				logger.debug("mail[{0}] subject[{1}] unmatch[{2}][{3}].".format(index, subject, matchtype, temple))
	return (0, 0)

def  SaveMailAttach(LOGNAME, MAXMAILCOUNT, SAVEPATH, SAVETYPE):
	global logger
	logger = dunhe_public.SetLog(LOGNAME)
	global MAX_MAIL_COUNT
	MAX_MAIL_COUNT = MAXMAILCOUNT
	global SAVE_PATH
	SAVE_PATH = SAVEPATH

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
		sql_server = "SELECT ts.id, ts.Address, ts.ServerName, ts.Username, ts.`Password`, ts.Use_SSL, ts.port from ServerInfo ts WHERE ServerName = \'Settlement\';"
		if SAVETYPE == "PreNetTable":
			sql_mailsubject = "SELECT t1.FundName, t1.PreNetSubject, t1.PreNetSubjectMatchType from FundInfo_ALL t1 WHERE t1.IsPreNet = 1 and t1.valid = 1 \
							UNION ALL \
							SELECT t2.FundName, t2.NetSubject, t2.NetSubjectMatchType from FundInfo_ALL t2 WHERE t2.IsPreNet = 0 and t2.PreNetRenameMatchType != 0 and t2.valid = 1;"
		elif SAVETYPE == "NetTable":
			sql_mailsubject = "SELECT t.FundName, t.NetSubject, t.NetSubjectMatchType from FundInfo_ALL t WHERE t.valid = 1;"
		else:
			return

		try:
			#对接邮件服务器解析邮件
			logger.debug("execute sql: " + sql_server)
			cursor.execute(sql_server)
			serverdata = cursor.fetchall()
			logger.debug("Get mail server info:%s" % serverdata)
			#先把主题的匹配内容，匹配规则取出来
			logger.debug("execute sql: " + sql_mailsubject)
			cursor.execute(sql_mailsubject)
			mailsubjectdata = cursor.fetchall()
			logger.debug("Match table: {0}".format(mailsubjectdata))
			#关闭数据库
			cursor.close()
			connection.close()
		except Exception as e:
			logger.error("Sql execute error: {0}".format(e))

	if serverdata:
		serverinfo = serverdata[0]
		logger.debug("Get one mail server info: {0}".format(serverinfo))
	else:
		serverinfo = (0, 'pop.exmail.qq.com', 'Settlement', 'settlement@dunhefund.com', 'Ff112113', '1', '995')

	ConnectResult = Connect2Mailserver(serverinfo)
	if not ConnectResult[0]:
		logger.error("Connect to server fail: %s" % ConnectResult[1])
	else:
		try:
			server = ConnectResult[1]
			if not mailsubjectdata:
				logger.error("No subject data!")
				sys.exit()

			#MatchTable增加核对结果列
			tupResult = ['0']
			listMatchTable = []
			for i in range(0, len(mailsubjectdata)):
				listMatchTable.append(list(mailsubjectdata[i]) + tupResult)

			#如果解析出了问题，会返回1，这里需要重试
			parseResult = ParseMail(server, listMatchTable)
			while parseResult[0]:
				index = parseResult[1]
				server.quit()
				server = Connect2Mailserver(serverinfo)[1]
				parseResult = ParseMail(server, listMatchTable, index)
		except Exception as e:
			logger.error("Connect/parse mail error:{0}".format(e))
			raise e
		finally:
			server.quit()

	logger.info("Mail save result:")
	iSuccess = 0
	for fundname, temple, matchtype, matchresult in listMatchTable:
		if matchresult == '1':
			iSuccess += 1
			logger.info("{0} Get {1} Successfully!".format(fundname, SAVETYPE))
		else:
			logger.info("{0} Get {1} Fail!".format(fundname, SAVETYPE))
	logger.info("Get success[{0}], fail[{1}], total[{2}]".format(iSuccess, len(listMatchTable) - iSuccess, len(listMatchTable)))
	logger.info("Mail save over!")
