import os, sys, string
import poplib
import email

class Pop3Client:
    ServerAddress = ""
    Port = 0
    SSL = True
    Name = ""
    Password = ""
    def connect(self):
        if ServerAddress == "":
            return "ServerAddress is NULL"
        if Port == 0:
            return "Port is 0"
        if Name == "":
            return "Name is NULL"
        if Password == "":
            return "Password is NULL"

        try:
            client = poplib.POP3(ServerAddress)
            client.user(Name)
            client.pass_(Password)
        except Exception as ex:
            errmsg = str(bytes(ex.args[0]), "gb2312")   
            return("Logon server fail: ", errmsg)

        return