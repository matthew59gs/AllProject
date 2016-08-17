#include <iostream>
#include <string>
#include "spi.h"
#include ".\API\ThostFtdcTraderApi.h"

using namespace std;

int iRequestID;			// ������

// �Ự����
TThostFtdcFrontIDType	FRONT_ID;	//ǰ�ñ��
TThostFtdcSessionIDType	SESSION_ID;	//�Ự���
TThostFtdcOrderRefType	ORDER_REF;	//��������

void CTraderSpi::stopAPI()
{
	SetEvent(g_hEvent);
}

bool CTraderSpi::IsErrorRspInfo(CThostFtdcRspInfoField *pRspInfo)
{
	// ���ErrorID != 0, ˵���յ��˴������Ӧ
	bool bResult = ((pRspInfo) && (pRspInfo->ErrorID != 0));
	if (bResult)
		cout << "--->>> ErrorID=" << pRspInfo->ErrorID << ", ErrorMsg=" << pRspInfo->ErrorMsg << endl;
	return bResult;
}

void CTraderSpi::OnFrontConnected()
{
	cout << "--->>> " << "OnFrontConnected" << endl;
	///�û���¼����
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
	cout << "--->>> �����û���¼����: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin,
	CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspUserLogin" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		// ����Ự����
		FRONT_ID = pRspUserLogin->FrontID;
		SESSION_ID = pRspUserLogin->SessionID;
		int iNextOrderRef = atoi(pRspUserLogin->MaxOrderRef);
		iNextOrderRef++;
		sprintf_s(ORDER_REF, "%d", iNextOrderRef);
		///��ȡ��ǰ������
		cout << "--->>> ��ȡ��ǰ������ = " << pUserApi->GetTradingDay() << endl;
		Sleep(1000);
		///Ͷ���߽�����ȷ��
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
	cout << "--->>> Ͷ���߽�����ȷ��: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspSettlementInfoConfirm" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		Sleep(1000);
		///�����ѯ�˻�
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
	cout << "--->>> �����ѯ�ʽ��˻�: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspQryTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryTradingAccount" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		cout << "--->>> �ʽ��ʺ���Ϣ��" << endl;
		cout << "�˻��ţ�" << pTradingAccount->AccountID << endl;
		cout << "��" << pTradingAccount->Balance << endl;
		cout << "ƽ�����棺" << pTradingAccount->CloseProfit << endl;
		cout << "��ǰռ�ñ�֤��" << pTradingAccount->CurrMargin << endl;
		cout << "�����ţ�" << pTradingAccount->SettlementID << endl;
		cout << "��Ϣ���ڣ�" << pTradingAccount->TradingDay << endl;

		///�����ѯͶ���ֲ߳�
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
	cout << "--->>> �����ѯͶ���ֲ߳�: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryInvestorPosition" << endl;
	if (!IsErrorRspInfo(pRspInfo))
	{
		if (pInvestorPosition != NULL)
		{
			///��Լ����
			cout << "****��Լ���룺" << pInvestorPosition->InstrumentID << endl;
			///���ճֲ�
			cout << "****�ֲ�����" << pInvestorPosition->Position << endl;
			///��շ��� 2����ͷ��3����ͷ
			if (pInvestorPosition->PosiDirection == '2')
				cout << "****��շ��򣺶�ͷ" << endl;
			else
				cout << "****��շ��򣺿�ͷ" << endl;
			///��������֤��
			cout << "****��������֤��" << pInvestorPosition->ExchangeMargin << endl;
		}

		if (bIsLast)
		{
			Sleep(1000);
			///�����ѯͶ���߽�����
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
	cout << "--->>> �����ѯͶ���߽�����: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspQrySettlementInfo(CThostFtdcSettlementInfoField *pSettlementInfo, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQrySettlementInfo" << endl;
	if (bIsLast && !IsErrorRspInfo(pRspInfo))
	{
		Sleep(1000);
		///�����ѯ���ױ���
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
	cout << "--->>> �����ѯ���ױ���: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspQryTradingCode(CThostFtdcTradingCodeField *pTradingCode, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryTradingCode" << endl;
	if (!IsErrorRspInfo(pRspInfo))
	{
		if (pTradingCode != NULL)
		{
			cout << "--->>> ���ױ�����Ϣ��" << endl;
			cout << "���ױ��룺" << pTradingCode->ClientID << endl;
			cout << "��������" << pTradingCode->ExchangeID << endl;
			cout << "�ͻ��ţ�" << pTradingCode->InvestorID << endl;
			cout << "�Ƿ��Ծ��" << ((pTradingCode->IsActive == 1) ? "��" : "��") << endl;
		}

		if (bIsLast)
		{
			cout << "��ѯ����" << endl;

			char c_result;
			cout << "�Ƿ��ѯ��֤�������Y/N����" << endl;
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
	cout << "--->>> �����ѯ��֤�����: " << ((iResult == 0) ? "�ɹ�" : "ʧ��") << endl;
}

void CTraderSpi::OnRspQryInstrument(CThostFtdcInstrumentField *pInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	cout << "--->>> " << "OnRspQryInstrument" << endl;
	if (!IsErrorRspInfo(pRspInfo))
	{
		if (pInstrument != NULL)
		{
			cout << "--->>> ��֤�������Ϣ��" << endl;
			cout << "��Լ���룺" << pInstrument->InstrumentID << endl;
			cout << "��������" << pInstrument->ExchangeID << endl;
			cout << "��ͷ��֤�������" << pInstrument->LongMarginRatio << endl;
			cout << "��ͷ��֤�����" << pInstrument->ShortMarginRatio << endl;
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