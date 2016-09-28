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
	///�ڻ���˾����
	TUserDefBrokerName BrokerName;
	///���͹�˾����
	TThostFtdcBrokerIDType	BrokerID;
	//����ǰ�õ�ַ tcp://192.1.1.1:1028
	TUserDefFrontAddr FrontAddress;
	///�û�����
	TThostFtdcUserIDType	UserID;
	///����
	TThostFtdcPasswordType	Password;
	///�û��˲�Ʒ��Ϣ
	TThostFtdcProductInfoType	UserProductInfo;
};

typedef vector<TUserDefLoginInfo> VUserDefBroker;

// USER_API����
extern CThostFtdcTraderApi* pUserApi;

// HANDLE
extern HANDLE g_hEvent;

// ���ò���
extern char FRONT_ADDR[];		// ǰ�õ�ַ
extern char BROKER_ID[];		// ���͹�˾����
extern char INVESTOR_ID[];		// Ͷ���ߴ���
extern char PASSWORD[];		// �û�����
//char INSTRUMENT_ID[];	// ��Լ����
extern char UserProductInfo[];		// �û����

extern int iRequestID;			// ������

// �Ự����
extern TThostFtdcFrontIDType	FRONT_ID;	//ǰ�ñ��
extern TThostFtdcSessionIDType	SESSION_ID;	//�Ự���
extern TThostFtdcOrderRefType	ORDER_REF;	//��������

// ѡ��ȯ��
int ChooseBrokerShow();

class CTraderSpi : public CThostFtdcTraderSpi
{
public:
	///���ͻ����뽻�׺�̨������ͨ������ʱ����δ��¼ǰ�����÷��������á�
	virtual void OnFrontConnected();

	///��¼������Ӧ
	virtual void OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///Ͷ���߽�����ȷ����Ӧ
	virtual void OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///�����ѯ�ʽ��˻���Ӧ
	virtual void OnRspQryTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///�����ѯͶ���ֲ߳���Ӧ
	virtual void OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///�����ѯ���ױ�����Ӧ
	virtual void OnRspQryTradingCode(CThostFtdcTradingCodeField *pTradingCode, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///�����ѯͶ���߽�������Ӧ
	virtual void OnRspQrySettlementInfo(CThostFtdcSettlementInfoField *pSettlementInfo, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///�����ѯ��֤�������Ӧ
	virtual void OnRspQryInstrument(CThostFtdcInstrumentField *pInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///�����ѯ��Լ����
	virtual void OnRspQryInstrumentCommissionRate(CThostFtdcInstrumentCommissionRateField *pInstrumentCommissionRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///����Ӧ��
	virtual void OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

	///���ͻ����뽻�׺�̨ͨ�����ӶϿ�ʱ���÷��������á���������������API���Զ��������ӣ��ͻ��˿ɲ�������
	virtual void OnFrontDisconnected(int nReason);

	///������ʱ���档����ʱ��δ�յ�����ʱ���÷��������á�
	virtual void OnHeartBeatWarning(int nTimeLapse);

private:
	///�û���¼����
	void ReqUserLogin();
	///Ͷ���߽�����ȷ��
	void ReqSettlementInfoConfirm();
	///�����ѯ��Լ
	void ReqQryInstrument();
	///�����ѯ�ʽ��˻�
	void ReqQryTradingAccount();
	////�����ѯ���ױ���
	void ReqQryTradingCode();
	///�����ѯͶ���ֲ߳�
	void ReqQryInvestorPosition();
	///�����ѯͶ���߽�����
	void ReqQrySettlementInfo();
	///��ѯ����
	void ReqQryInstrumentCommissionRate();

	// �Ƿ��յ��ɹ�����Ӧ
	bool IsErrorRspInfo(CThostFtdcRspInfoField *pRspInfo);

	// ֪ͨ���̼߳���
	void stopAPI();
};

#endif