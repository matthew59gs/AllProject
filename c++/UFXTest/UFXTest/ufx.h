#pragma once

#ifndef UFX_H
#define UFX_H

#include <string>
#include "t2sdk_interface.h"

class CErrorInfo
{
public:
	CErrorInfo() :ErrorCode(0), ErrorMsg("") {}
	int    ErrorCode;
	string ErrorMsg;
};

class UFX
{
public:
	std::string address;
	void say_hello(void)
	{
		printf("hello from UFXTest!\n");
	}
};

void       ShowPacket(IF2UnPacker* unPacker);
CErrorInfo Connect(const char* serverAddr, CConnectionInterface** connection);
CErrorInfo Login(CConnectionInterface* connection, const char* operatorNo, const char* password, string& userToken);
CErrorInfo Entrust(CConnectionInterface* connection, const char* userToken, const char* combiNo, const char* marketNo, const char* stockCode, const char* entrustDirection, double entrustPrice, int entrustAmount, int& entrustNo);
CErrorInfo QueryEntrusts(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker);
CErrorInfo QueryDeals(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker);
CErrorInfo QueryAccount(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, IF2UnPacker** responseUnPacker);
CErrorInfo QueryCombiStock(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode, IF2UnPacker** responseUnPacker);
void       HeartBeat(CConnectionInterface* connection, const char* userToken);

#endif