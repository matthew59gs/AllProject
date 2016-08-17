#include <iostream>
#include <string>
#include "spi.h"
#include ".\API\ThostFtdcTraderApi.h"

using namespace std;

int iRequestID;			// 请求编号

// 会话参数
TThostFtdcFrontIDType	FRONT_ID;	//前置编号
TThostFtdcSessionIDType	SESSION_ID;	//会话编号
TThostFtdcOrderRefType	ORDER_REF;	//报单引用

void CTraderSpi::stopAPI()
{
	SetEvent(g_hEvent);
}

bool CTraderSpi::IsErrorRspInfo(CThostFtdcRspInfoField *pRspInfo)
{
	// 如果ErrorID != 0, 说明收到了错误的响应
	bool bResult = ((pRspInfo) && (pRspInfo->ErrorID != 0));
	if (bResult)
		cout << "--->>> ErrorID=" << pRspInfo->ErrorID << ", ErrorMsg=" << pRspInfo->ErrorMsg << endl;
	return bResult;
}

void CTraderSpi::OnFrontConnected()
{
	cout << "--->>> " << "OnFrontConnected" << endl;
	///用户登录请求
	ReqUserLogin();
}

void CTraderSpi::ReqUserLogin()
{
	CThostFtdcReqUserLoginField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.UserID, INVESTOR_ID);
	strcpy_s(req.Password, PASSWORD);
	strcpy_s(req.UserProductInfo, UserProductInfo);
	int iResult = pUserApi->ReqUserLogin(&req, ++iRequestID);
	cout << "--->>> 发送用户登录请求: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin,
	CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspUserLogin" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		// 保存会话参数
		FRONT_ID = pRspUserLogin->FrontID;
		SESSION_ID = pRspUserLogin->SessionID;
		int iNextOrderRef = atoi(pRspUserLogin->MaxOrderRef);
		iNextOrderRef++;
		sprintf_s(ORDER_REF, "%d", iNextOrderRef);
		///获取当前交易日
		cout << "--->>> 获取当前交易日 = " << pUserApi->GetTradingDay() << endl;
		Sleep(1000);
		///投资者结算结果确认
		ReqSettlementInfoConfirm();
	}
}

void CTraderSpi::ReqSettlementInfoConfirm()
{
	CThostFtdcSettlementInfoConfirmField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.InvestorID, INVESTOR_ID);
	int iResult = pUserApi->ReqSettlementInfoConfirm(&req, ++iRequestID);
	cout << "--->>> 投资者结算结果确认: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspSettlementInfoConfirm" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		Sleep(1000);
		///请求查询账户
		ReqQryTradingAccount();
	}
}

void CTraderSpi::ReqQryTradingAccount()
{
	CThostFtdcQryTradingAccountField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.InvestorID, INVESTOR_ID);
	int iResult = pUserApi->ReqQryTradingAccount(&req, ++iRequestID);
	cout << "--->>> 请求查询资金账户: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspQryTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryTradingAccount" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		cout << "--->>> 资金帐号信息：" << endl;
		cout << "账户号：" << pTradingAccount->AccountID << endl;
		cout << "金额：" << pTradingAccount->Balance << endl;
		cout << "平仓收益：" << pTradingAccount->CloseProfit << endl;
		cout << "当前占用保证金：" << pTradingAccount->CurrMargin << endl;
		cout << "结算编号：" << pTradingAccount->SettlementID << endl;
		cout << "信息日期：" << pTradingAccount->TradingDay << endl;

		///请求查询投资者持仓
		Sleep(1000);
		ReqQryInvestorPosition();
	}
}

void CTraderSpi::ReqQryInvestorPosition()
{
	CThostFtdcQryInvestorPositionField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.InvestorID, INVESTOR_ID);
	//strcpy(req.InstrumentID, INSTRUMENT_ID);
	int iResult = pUserApi->ReqQryInvestorPosition(&req, ++iRequestID);
	cout << "--->>> 请求查询投资者持仓: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryInvestorPosition" << endl;
	if (!IsErrorRspInfo(pRspInfo))
	{
		if (pInvestorPosition != NULL)
		{
			///合约代码
			cout << "****合约代码：" << pInvestorPosition->InstrumentID << endl;
			///今日持仓
			cout << "****持仓量：" << pInvestorPosition->Position << endl;
			///多空方向 2：多头；3：空头
			if (pInvestorPosition->PosiDirection == '2')
				cout << "****多空方向：多头" << endl;
			else
				cout << "****多空方向：空头" << endl;
			///交易所保证金
			cout << "****交易所保证金：" << pInvestorPosition->ExchangeMargin << endl;
		}

		if (bIsLast)
		{
			Sleep(1000);
			///请求查询投资者结算结果
			ReqQrySettlementInfo();
		}
	}
}

void CTraderSpi::ReqQrySettlementInfo()
{
	CThostFtdcQrySettlementInfoField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.InvestorID, INVESTOR_ID);
	int iResult = pUserApi->ReqQrySettlementInfo(&req, ++iRequestID);
	cout << "--->>> 请求查询投资者结算结果: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspQrySettlementInfo(CThostFtdcSettlementInfoField *pSettlementInfo, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQrySettlementInfo" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		Sleep(1000);
		///请求查询交易编码
		ReqQryTradingCode();
	}
}

void CTraderSpi::ReqQryTradingCode()
{
	CThostFtdcQryTradingCodeField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.InvestorID, INVESTOR_ID);
	int iResult = pUserApi->ReqQryTradingCode(&req, ++iRequestID);
	cout << "--->>> 请求查询交易编码: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspQryTradingCode(CThostFtdcTradingCodeField *pTradingCode, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryTradingCode" << endl;
	if (!IsErrorRspInfo(pRspInfo))
	{
		if (pTradingCode != NULL)
		{
			cout << "--->>> 交易编码信息：" << endl;
			cout << "交易编码：" << pTradingCode->ClientID << endl;
			cout << "交易所：" << pTradingCode->ExchangeID << endl;
			cout << "客户号：" << pTradingCode->InvestorID << endl;
			cout << "是否活跃：" << ((pTradingCode->IsActive == 1) ? "是" : "否") << endl;
		}

		if (bIsLast)
		{
			cout << "查询结束" << endl;

			char c_result;
			cout << "是否查询保证金比例（Y/N）：" << endl;
			cin >> c_result;
			if ('Y' == c_result || 'y' == c_result)
				ReqQryInstrument();
			else
				stopAPI();
		}
	}
	else
		stopAPI();
}

void CTraderSpi::ReqQryInstrument()
{
	CThostFtdcQryInstrumentField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.InstrumentID, "SR711");
	int iResult = pUserApi->ReqQryInstrument(&req, ++iRequestID);
	cout << "--->>> 请求查询保证金比例: " << ((iResult == 0) ? "成功" : "失败") << endl;
}

void CTraderSpi::OnRspQryInstrument(CThostFtdcInstrumentField *pInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryInstrument" << endl;
	if (!IsErrorRspInfo(pRspInfo))
	{
		if (pInstrument != NULL)
		{
			cout << "--->>> 保证金比例信息：" << endl;
			cout << "合约代码：" << pInstrument->InstrumentID << endl;
			cout << "交易所：" << pInstrument->ExchangeID << endl;
			cout << "多头保证金比例：" << pInstrument->LongMarginRatio << endl;
			cout << "空头保证金比例" << pInstrument->ShortMarginRatio << endl;
		}

		string end;
		cin >> end;

		if (bIsLast)
				stopAPI();
	}
	else
		stopAPI();
}

void CTraderSpi::OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspError" << endl;
	IsErrorRspInfo(pRspInfo);
}

void CTraderSpi::OnFrontDisconnected(int nReason)
{
	cout << "--->>> " << "OnFrontDisconnected" << endl;
	cout << "--->>> Reason = " << nReason << endl;
}

void CTraderSpi::OnHeartBeatWarning(int nTimeLapse)
{
	cout << "--->>> " << "OnHeartBeatWarning" << endl;
	cout << "--->>> nTimerLapse = " << nTimeLapse << endl;
}