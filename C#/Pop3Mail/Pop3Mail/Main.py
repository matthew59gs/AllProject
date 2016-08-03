# -*- coding: utf-8 -*-

import os, sys, string
import poplib
import email
import codecs
import array

ServerAddress = "pop.exmail.qq.com"
Name = "gaos@dunhefund.com"
Password = "123456"

def ssl_connect(ServerAddress, Name, Password):
    if ServerAddress == "":
        return "ServerAddress is NULL"
    if Port == 0:
        return "Port is 0"
    if Name == "":
        return "Name is NULL"
    if Password == "":
        return "Password is NULL"

    try:
        client = poplib.POP3_SSL(ServerAddress)
        client.user(Name)
        client.pass_(Password)
    except Exception as ex:
        errmsg = str(bytes(ex.args[0]), "gb2312")   
        print("Logon server fail:", ServerAddress, "失败:\n", errmsg)

ret = pp.stat()
print(ret)
