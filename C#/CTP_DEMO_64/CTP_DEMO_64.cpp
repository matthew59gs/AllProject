// CTP_DEMO.cpp : 定义控制台应用程序的入口点。
//

#include <iostream>
#include <list>
#include <Windows.h>
#include "spi.h"
#include ".\API\ThostFtdcTraderApi.h"

using namespace std;

// USER_API参数
CThostFtdcTraderApi* pUserApi;

// Create a manual reset event with no signal
HANDLE g_hEvent = CreateEvent(NULL, true, false, NULL);

// 券商信息
VUserDefBroker vBrokerList;

char  FRONT_ADDR[40];							// 前置地址
TThostFtdcBrokerIDType	BROKER_ID;				// 经纪公司代码
TThostFtdcInvestorIDType INVESTOR_ID;			// 投资者代码
TThostFtdcPasswordType  PASSWORD;				// 用户密码
TThostFtdcProductInfoType UserProductInfo;		// 产品信息

int main()
{
	if (ChooseBrokerShow())
		return 0;

	// 初始化UserApi
	pUserApi = CThostFtdcTraderApi::CreateFtdcTraderApi();			// 创建UserApi
	CTraderSpi* pUserSpi = new CTraderSpi();
	pUserApi->RegisterSpi((CThostFtdcTraderSpi*)pUserSpi);			// 注册事件类
	pUserApi->SubscribePublicTopic(THOST_TERT_RESTART);					// 注册公有流
	pUserApi->SubscribePrivateTopic(THOST_TERT_RESTART);					// 注册私有流
	pUserApi->RegisterFront(FRONT_ADDR);							// connect
	pUserApi->Init();

	//pUserApi->Join();
	WaitForSingleObject(g_hEvent, INFINITE);
	pUserApi->Release();

    return 0;
}

int ChooseBrokerShow()
{
	TUserDefLoginInfo *pBrokerInfo;
	// 永安测试信息
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "永安期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "1032");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://115.238.53.139:51205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "100502828");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "888888");				// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "Oplus");		// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 大越测试信息
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "大越期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "0023");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://101.231.85.169:31800");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "8990");					// 投资者代码
	strcpy_s(pBrokerInfo->Password, "236236");				// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 东证测试信息
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "东证期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "6666");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://180.166.103.34:41205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "66612157");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "dzqh123456");			// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 国泰君安期货测试信息
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "国泰君安期货测试");	// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "2071");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://180.169.77.111:42205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "82100519");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "888888");				// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "Oplus");		// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 海通期货测试信息
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "海通期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "8000");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://27.115.78.154:31205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "41003611");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "070617");				// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 中粮期货测试信息
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "中粮期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "8888");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://27.115.56.210:41205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "18906015");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "999999");				// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 浙商期货
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "浙商期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "6010");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://122.224.243.43:51205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "60300156");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "666666");				// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "Oplus");		// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 南华期货
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "南华期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "1008");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://115.238.106.253:41213");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "90094234");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "dunhe@123");			// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 五矿期货
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "五矿期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "8899");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://101.231.127.56:51205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "88888888");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "888888");			// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 大地期货
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "大地期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "0177");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://122.224.174.150:41205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "10000129");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "123456");			// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// 国投安信期货
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "国投安信期货测试");		// 经纪公司名称
	strcpy_s(pBrokerInfo->BrokerID, "4500");				// 经纪公司代码
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://27.115.97.3:41205");	// 前置地址
	strcpy_s(pBrokerInfo->UserID, "191");				// 投资者代码
	strcpy_s(pBrokerInfo->Password, "888888");			// 用户密码
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// 产品信息
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	cout << "请选择要查询的券商信息" << endl;
	unsigned int i, iInput, iIndex;
	for (i = 0; i < vBrokerList.size(); ++i)
	{
		cout << "[" << i + 1 << "] " << vBrokerList[i].BrokerName << endl;
	}
	cout << "请输入以上券商编号:";
	cin >> iInput;
	if (iInput > 0 && iInput <= i)
	{
		iIndex = iInput - 1;
		cout << "您选择了[" << iInput << "]" << vBrokerList[iIndex].BrokerName << endl;
		cout << "IP:" << vBrokerList[iIndex].FrontAddress << endl;

		strcpy_s(FRONT_ADDR, vBrokerList[iIndex].FrontAddress);			// 前置地址
		strcpy_s(BROKER_ID, vBrokerList[iIndex].BrokerID);					// 经纪公司代码
		strcpy_s(INVESTOR_ID, vBrokerList[iIndex].UserID);					// 投资者代码
		strcpy_s(PASSWORD, vBrokerList[iIndex].Password);					// 用户密码
		strcpy_s(UserProductInfo, vBrokerList[iIndex].UserProductInfo);	// 产品信息
		return 0;
	}
	else
		return -1;
}