// CTP_DEMO.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include <iostream>
#include <list>
#include <Windows.h>
#include "spi.h"
#include ".\API\ThostFtdcTraderApi.h"

using namespace std;

// USER_API����
CThostFtdcTraderApi* pUserApi;

// Create a manual reset event with no signal
HANDLE g_hEvent = CreateEvent(NULL, true, false, NULL);

// ȯ����Ϣ
VUserDefBroker vBrokerList;

char  FRONT_ADDR[40];							// ǰ�õ�ַ
TThostFtdcBrokerIDType	BROKER_ID;				// ���͹�˾����
TThostFtdcInvestorIDType INVESTOR_ID;			// Ͷ���ߴ���
TThostFtdcPasswordType  PASSWORD;				// �û�����
TThostFtdcProductInfoType UserProductInfo;		// ��Ʒ��Ϣ

int main()
{
	if (ChooseBrokerShow())
		return 0;

	// ��ʼ��UserApi
	pUserApi = CThostFtdcTraderApi::CreateFtdcTraderApi();			// ����UserApi
	CTraderSpi* pUserSpi = new CTraderSpi();
	pUserApi->RegisterSpi((CThostFtdcTraderSpi*)pUserSpi);			// ע���¼���
	pUserApi->SubscribePublicTopic(THOST_TERT_RESTART);					// ע�ṫ����
	pUserApi->SubscribePrivateTopic(THOST_TERT_RESTART);					// ע��˽����
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
	// ����������Ϣ
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "�����ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "1032");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://115.238.53.139:51205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "100502828");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "888888");				// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "Oplus");		// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ��Խ������Ϣ
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "��Խ�ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "0023");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://101.231.85.169:31800");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "8990");					// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "236236");				// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ��֤������Ϣ
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "��֤�ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "6666");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://180.166.103.34:41205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "66612157");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "dzqh123456");			// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ��̩�����ڻ�������Ϣ
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "��̩�����ڻ�����");	// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "2071");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://180.169.77.111:42205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "82100519");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "888888");				// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "Oplus");		// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ��ͨ�ڻ�������Ϣ
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "��ͨ�ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "8000");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://27.115.78.154:31205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "41003611");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "070617");				// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// �����ڻ�������Ϣ
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "�����ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "8888");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://27.115.56.210:41205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "18906015");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "999999");				// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// �����ڻ�
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "�����ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "6010");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://122.224.243.43:51205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "60300156");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "666666");				// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "Oplus");		// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// �ϻ��ڻ�
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "�ϻ��ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "1008");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://115.238.106.253:41213");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "90094234");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "dunhe@123");			// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ����ڻ�
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "����ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "8899");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://101.231.127.56:51205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "88888888");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "888888");			// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ����ڻ�
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "����ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "0177");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://122.224.174.150:41205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "10000129");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "123456");			// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	// ��Ͷ�����ڻ�
	pBrokerInfo = new TUserDefLoginInfo;
	strcpy_s(pBrokerInfo->BrokerName, "��Ͷ�����ڻ�����");		// ���͹�˾����
	strcpy_s(pBrokerInfo->BrokerID, "4500");				// ���͹�˾����
	strcpy_s(pBrokerInfo->FrontAddress, "tcp://27.115.97.3:41205");	// ǰ�õ�ַ
	strcpy_s(pBrokerInfo->UserID, "191");				// Ͷ���ߴ���
	strcpy_s(pBrokerInfo->Password, "888888");			// �û�����
	strcpy_s(pBrokerInfo->UserProductInfo, "");				// ��Ʒ��Ϣ
	vBrokerList.push_back(*pBrokerInfo);
	pBrokerInfo = NULL;

	cout << "��ѡ��Ҫ��ѯ��ȯ����Ϣ" << endl;
	unsigned int i, iInput, iIndex;
	for (i = 0; i < vBrokerList.size(); ++i)
	{
		cout << "[" << i + 1 << "] " << vBrokerList[i].BrokerName << endl;
	}
	cout << "����������ȯ�̱��:";
	cin >> iInput;
	if (iInput > 0 && iInput <= i)
	{
		iIndex = iInput - 1;
		cout << "��ѡ����[" << iInput << "]" << vBrokerList[iIndex].BrokerName << endl;
		cout << "IP:" << vBrokerList[iIndex].FrontAddress << endl;

		strcpy_s(FRONT_ADDR, vBrokerList[iIndex].FrontAddress);			// ǰ�õ�ַ
		strcpy_s(BROKER_ID, vBrokerList[iIndex].BrokerID);					// ���͹�˾����
		strcpy_s(INVESTOR_ID, vBrokerList[iIndex].UserID);					// Ͷ���ߴ���
		strcpy_s(PASSWORD, vBrokerList[iIndex].Password);					// �û�����
		strcpy_s(UserProductInfo, vBrokerList[iIndex].UserProductInfo);	// ��Ʒ��Ϣ
		return 0;
	}
	else
		return -1;
}