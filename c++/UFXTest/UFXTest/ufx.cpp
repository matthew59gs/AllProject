#include "ufx.h"
#include <iostream>
#include <synchapi.h>
#include <process.h>

using namespace std;

void ShowPacket(IF2UnPacker* unPacker)
{
	int i = 0, t = 0, j = 0, k = 0;
	FILE *fp;
	fp = fopen("test.csv", "w");

	for (i = 1; i < unPacker->GetDatasetCount(); ++i)
	{
		printf("%d", i);
		// ���õ�ǰ�����
		unPacker->SetCurrentDatasetByIndex(i);

		// ��ӡ�ֶ�
		for (t = 0; t < unPacker->GetColCount(); ++t)
		{
			fprintf(fp, "%s,", unPacker->GetColName(t));
		}
		fprintf(fp, "\n");

		// ��ӡ���м�¼
		for (j = 0; j < (int)unPacker->GetRowCount(); ++j)
		{
			// ��ӡÿ����¼
			for (k = 0; k < unPacker->GetColCount(); ++k)
			{
				switch (unPacker->GetColType(k))
				{
				case 'I':
					fprintf(fp, "%d,", unPacker->GetIntByIndex(k));
					break;

				case 'C':
					fprintf(fp, "%c,", unPacker->GetCharByIndex(k));
					break;

				case 'S':
					fprintf(fp, "%s,", unPacker->GetStrByIndex(k));
					break;

				case 'F':
					fprintf(fp, "%f,", unPacker->GetDoubleByIndex(k));
					break;

				case 'R':
				{
					int nLength = 0;
					void *lpData = unPacker->GetRawByIndex(k, &nLength);

					// ��2�������ݽ��д���
					break;
				}

				default:
					// δ֪��������
					printf("δ֪�������͡�\n");
					break;
				}
			}

			fprintf(fp, "\n");
			unPacker->Next();
		}

		fprintf(fp, "\n");

	}
	fclose(fp);
}

CErrorInfo GetErrorInfo(IF2UnPacker* responseUnPacker)
{
	CErrorInfo errorInfo;
	errorInfo.ErrorCode = responseUnPacker->GetInt("ErrorCode");
	if (responseUnPacker->GetStr("ErrorMsg"))
		errorInfo.ErrorMsg = responseUnPacker->GetStr("ErrorMsg");
	return errorInfo;
}

CErrorInfo CallService(CConnectionInterface* connection, int functionNo, IF2Packer* requestPacker, IF2UnPacker** responseUnPacker)
{
	CErrorInfo errorInfo;
	int ret = connection->SendBiz(functionNo, requestPacker);
	if (ret > 0)
	{
		void* Pointer;
		ret = connection->RecvBiz(ret, &Pointer, 3000);
		switch (ret)
		{
		case 0:
		case 1:
			//Ӧ���һ������������ݼ���
			//��һ�����ݼ���ͷ����Ϣ��������ErrorCode��ErrorMsg����Ϣ
			//�ڶ������ݼ�����������ҵ������
			(*responseUnPacker) = (IF2UnPacker*)Pointer;
			errorInfo = GetErrorInfo(*responseUnPacker);
			if ((*responseUnPacker)->GetDatasetCount() > 1) (*responseUnPacker)->SetCurrentDatasetByIndex(1);
			break;
		case 2:
			errorInfo.ErrorCode = 2;
			errorInfo.ErrorMsg = (char*)Pointer;
			break;
		default:
			errorInfo.ErrorCode = 3;
			errorInfo.ErrorMsg = connection->GetErrorMsg(ret);
			break;

		}
	}
	else
	{
		errorInfo.ErrorCode = ret;
		errorInfo.ErrorMsg = connection->GetErrorMsg(ret);
	}
	return errorInfo;
}

CErrorInfo Connect(const char* serverAddr, CConnectionInterface** connection)
{
	CErrorInfo errorInfo;
	//����T2SDK���ö��󣬲�����UFX��������ַ�Լ�License�ļ�
	CConfigInterface * config = NewConfig();
	config->AddRef();
	config->Load("t2sdk.ini");

	//�������Ӷ��󣬲�����UFX������
	CConnectionInterface* conn = NewConnection(config);
	conn->AddRef();
	int ret = conn->Create(NULL);
	if (ret != 0)
	{
		errorInfo.ErrorCode = ret;
		errorInfo.ErrorMsg = conn->GetErrorMsg(ret);
		conn->Release();
		config->Release();
		return errorInfo;
	}

	//����UFX������������3000Ϊ��ʱ��������λ����
	ret = conn->Connect(3000);
	if (ret != 0)
	{
		errorInfo.ErrorCode = ret;
		errorInfo.ErrorMsg = conn->GetErrorMsg(ret);
		conn->Release();
		config->Release();
		return errorInfo;
	}

	config->Release();
	(*connection) = conn;
	return errorInfo;
}

IF2Packer* MakeLoginPacker(const char* operatorNo, const char* password)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("operator_no", 'S', 16, 0);
	requestPacker->AddField("password", 'S', 32, 0);
	requestPacker->AddField("mac_address", 'S', 255, 0);
	requestPacker->AddField("op_station", 'S', 255, 0);
	requestPacker->AddField("ip_address", 'S', 32, 0);
	requestPacker->AddField("authorization_id", 'S', 64, 0);
	requestPacker->AddStr(operatorNo);
	requestPacker->AddStr(password);
	requestPacker->AddStr("5C-26-0A-2F-82-4F");
	requestPacker->AddStr("192.168.88.123|5C-26-0A-2F-82-4F");
	requestPacker->AddStr("192.168.88.123");
	requestPacker->AddStr("hd123456");
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo GetUserToken(IF2UnPacker* responseUnPacker, string& userToken)
{
	CErrorInfo errorInfo;
	if (responseUnPacker->FindColIndex("user_token") >= 0)
	{
		userToken = responseUnPacker->GetStr("user_token");
	}
	else
	{
		errorInfo.ErrorCode = -100;
		errorInfo.ErrorMsg = "user_token�ֶ���Ӧ����в�����";
	}
	return errorInfo;
}

CErrorInfo Login(CConnectionInterface* connection, const char* operatorNo, const char* password, string& userToken)
{
	IF2Packer* lpRequestPacker = MakeLoginPacker(operatorNo, password);
	IF2UnPacker* lpUnPacker;
	//��¼���ܺţ�10001
	CErrorInfo errorInfo = CallService(connection, 10001, lpRequestPacker, &lpUnPacker);
	if (errorInfo.ErrorCode == 0)
	{
		errorInfo = GetUserToken(lpUnPacker, userToken);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeEntrustPacker(const char* userToken, const char* combiNo, const char* marketNo
	, const char* stockCode, const char* entrustDirection, double entrustPrice, int entrustAmount)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512, 0);
	requestPacker->AddField("combi_no", 'S', 8, 0);
	requestPacker->AddField("market_no", 'S', 3, 0);
	requestPacker->AddField("stock_code", 'S', 16, 0);
	requestPacker->AddField("entrust_direction", 'S', 1, 0);
	requestPacker->AddField("price_type", 'S', 1, 0);
	requestPacker->AddField("entrust_price", 'F', 9, 3);
	requestPacker->AddField("entrust_amount", 'F', 16, 2);
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(combiNo);
	requestPacker->AddStr(marketNo);
	requestPacker->AddStr(stockCode);
	requestPacker->AddStr(entrustDirection);
	requestPacker->AddStr("0");                  //�޼�
	requestPacker->AddDouble(entrustPrice);
	requestPacker->AddDouble(entrustAmount);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo GetEntrustNo(IF2UnPacker* responseUnPacker, int& entrustNo)
{
	CErrorInfo errorInfo;
	if (responseUnPacker->FindColIndex("entrust_no") >= 0)
	{
		entrustNo = responseUnPacker->GetInt("entrust_no");
	}
	else
	{
		errorInfo.ErrorCode = -100;
		errorInfo.ErrorMsg = "entrust_no�ֶ���Ӧ����в�����";
	}
	printf("%d", entrustNo);
	return errorInfo;
}

CErrorInfo Entrust(CConnectionInterface* connection, const char* userToken, const char* combiNo, const char* marketNo, const char* stockCode, const char* entrustDirection, double entrustPrice, int entrustAmount, int& entrustNo)
{
	IF2Packer* lpRequestPacker = MakeEntrustPacker(userToken, combiNo, marketNo, stockCode, entrustDirection, entrustPrice, entrustAmount);
	IF2UnPacker* lpUnPacker;
	//��¼���ܺţ�91001
	CErrorInfo errorInfo = CallService(connection, 91001, lpRequestPacker, &lpUnPacker);
	if (errorInfo.ErrorCode == 0)
	{
		errorInfo = GetEntrustNo(lpUnPacker, entrustNo);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryEntrustsPacker(const char* userToken, const char* accountCode, const char* combiNo, int entrustNo)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512);
	requestPacker->AddField("account_no", 'S', 32);
	requestPacker->AddField("combi_no", 'S', 8);
	requestPacker->AddField("entrust_no", 'I');
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->AddInt(entrustNo);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryEntrusts(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryEntrustsPacker(userToken, accountCode, combiNo, entrustNo);
	//ί�в�ѯ���ܺţ�32001
	CErrorInfo errorInfo = CallService(connection, 32001, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryDealsPacker(const char* userToken, const char* accountCode, const char* combiNo, int entrustNo)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512);
	requestPacker->AddField("account_code", 'S', 32);
	requestPacker->AddField("asset_no", 'S', 16);
	requestPacker->AddField("entrust_no", 'I');
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->AddInt(entrustNo);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryDeals(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryDealsPacker(userToken, accountCode, combiNo, entrustNo);

	//�ڻ���ѯ���ܺţ�33003
	CErrorInfo errorInfo = CallService(connection, 33003, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryAccountPacker(const char* userToken, const char* accountCode, const char* combiNo)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512);
	requestPacker->AddField("account_no", 'S', 32);
	requestPacker->AddField("combi_no", 'S', 8);
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryAccount(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryAccountPacker(userToken, accountCode, combiNo);
	//ί�в�ѯ���ܺţ�34001
	CErrorInfo errorInfo = CallService(connection, 34001, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryCombiStockPacker(const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512);
	requestPacker->AddField("account_no", 'S', 32);
	requestPacker->AddField("combi_no", 'S', 8);
	requestPacker->AddField("market_no", 'S', 3);
	requestPacker->AddField("stock_code", 'S', 16);
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->AddStr(marketNo);
	requestPacker->AddStr(stockCode);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryCombiStock(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryCombiStockPacker(userToken, accountCode, combiNo, marketNo, stockCode);
	//ί�в�ѯ���ܺţ�34001
	CErrorInfo errorInfo = CallService(connection, 34001, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeHeartBeatPacker(const char* userToken)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512);
	requestPacker->AddField("version_no", 'S', 512);
	requestPacker->AddStr(userToken);;
	requestPacker->AddStr("version_no");;
	requestPacker->EndPack();
	return requestPacker;
}

struct ThreadFuncParam
{
	CConnectionInterface* connection;
	string userToken;
};
void HeartBeatThreadFunc(void* lp)
{
	ThreadFuncParam* param = (ThreadFuncParam*)lp;
	CConnectionInterface* connection = param->connection;
	IF2Packer* lpRequestPacker = MakeHeartBeatPacker(param->userToken.c_str());
	IF2UnPacker* lpUnPacker;
	while (true)
	{
		//�������ܺţ�10000
		CallService(connection, 10000, lpRequestPacker, &lpUnPacker);
		Sleep(1000);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	delete param;
}

void HeartBeat(CConnectionInterface* connection, const char* userToken)
{
	ThreadFuncParam* param = new ThreadFuncParam();
	param->connection = connection;
	param->userToken = userToken;
	_beginthread(HeartBeatThreadFunc, 0, param);
}
