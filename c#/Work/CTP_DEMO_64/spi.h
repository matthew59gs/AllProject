#pragma once

#if !defined(CTP_DEMO_H )
#define CTP_DEMO_H  

#include ".\API\ThostFtdcTraderApi.h"
#include <Windows.h>
#include <vector>

using namespace std;

typedef char TUserDefBrokerName[64];
typedef char TUserDefFrontAddr[64];

class TUserDefLoginInfo
{
public:
	///期货公司名称
	TUserDefBrokerName BrokerName;
	///经纪公司代码
	TThostFtdcBrokerIDType	BrokerID;
	//交易前置地址 tcp://192.1.1.1:1028
	TUserDefFrontAddr FrontAddress;
	///用户代码
	TThostFtdcUserIDType	UserID;
	///密码
	TThostFtdcPasswordType	Password;
	///用户端产品信息
	TThostFtdcProductInfoType	UserProductInfo;
};

typedef vector<TUserDefLoginInfo> VUserDefBroker;

// USER_API参数
extern CThostFtdcTraderApi* pUserApi;

// HANDLE
extern HANDLE g_hEvent;

// 配置参数
extern char FRONT_ADDR[];		// 前置地址
extern char BROKER_ID[];		// 经纪公司代码
extern char INVESTOR_ID[];		// 投资者代码
extern char PASSWORD[];		// 用户密码
//char INSTRUMENT_ID[];	// 合约代码
extern char UserProductInfo[];		// 用户软件

extern int iRequestID;			// 请求编号

// 会话参数
extern TThostFtdcFrontIDType	FRONT_ID;	//前置编号
extern TThostFtdcSessionIDType	SESSION_ID;	//会话编号
extern TThostFtdcOrderRefType	ORDER_REF;	//报单引用

// 选择券商
int ChooseBrokerShow();

class CTraderSpi : public CThostFtdcTraderSpi
{
public:
	///当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
	virtual void OnFrontConnected();

	///登录请求响应
	virtual void OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///投资者结算结果确认响应
	virtual void OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///请求查询资金账户响应
	virtual void OnRspQryTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///请求查询投资者持仓响应
	virtual void OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///请求查询交易编码响应
	virtual void OnRspQryTradingCode(CThostFtdcTradingCodeField *pTradingCode, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///请求查询投资者结算结果响应
	virtual void OnRspQrySettlementInfo(CThostFtdcSettlementInfoField *pSettlementInfo, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///请求查询保证金比例响应
	virtual void OnRspQryInstrument(CThostFtdcInstrumentField *pInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///请求查询合约费率
	virtual void OnRspQryInstrumentCommissionRate(CThostFtdcInstrumentCommissionRateField *pInstrumentCommissionRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///错误应答
	virtual void OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
	virtual void OnFrontDisconnected(int nReason);

	///心跳超时警告。当长时间未收到报文时，该方法被调用。
	virtual void OnHeartBeatWarning(int nTimeLapse);

private:
	///用户登录请求
	void ReqUserLogin();
	///投资者结算结果确认
	void ReqSettlementInfoConfirm();
	///请求查询合约
	void ReqQryInstrument();
	///请求查询资金账户
	void ReqQryTradingAccount();
	////请求查询交易编码
	void ReqQryTradingCode();
	///请求查询投资者持仓
	void ReqQryInvestorPosition();
	///请求查询投资者结算结果
	void ReqQrySettlementInfo();
	///查询费率
	void ReqQryInstrumentCommissionRate();

	// 是否收到成功的响应
	bool IsErrorRspInfo(CThostFtdcRspInfoField *pRspInfo);

	// 通知主线程技术
	void stopAPI();
};

#endif