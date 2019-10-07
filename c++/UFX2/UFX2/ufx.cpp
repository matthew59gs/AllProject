#include "pch.h"
#include "ufx.h"
#include "Manager.h"

#include <process.h>
#include <stdlib.h>
#include <Windows.h>
#include <iostream>
#include <string>
using namespace std;

/*
** ufx
**/

ufx::~ufx()
{
	this->ReleaseConnection();
}

// private

IF2Packer* ufx::MakeLoginPacker(const char* operatorNo, const char* password)
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

IF2Packer* ufx:: MakeQueryEntrustsPacker(const char* userToken, const char* accountCode, const char* combiNo, int entrustNo) {
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

IF2Packer* ufx::MakeQueryDealsPacker(const char* userToken, const char* accountCode, const char* combiNo, int entrustNo)
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

IF2Packer* ufx:: MakeQueryAccountPacker(const char* userToken, const char* accountCode, const char* combiNo)
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

IF2Packer* ufx::MakeQueryCombiStockPacker(const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode)
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

IF2Packer* ufx::MakeHeartBeatPacker(const char* userToken)
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

IF2Packer* ufx::MakeCombiQuery(const char* userToken)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S', 512);
	requestPacker->AddStr(userToken);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo ufx::GetErrorInfo(IF2UnPacker* responseUnPacker)
{
	CErrorInfo errorInfo;
	errorInfo.ErrorCode = responseUnPacker->GetInt("ErrorCode");
	if (responseUnPacker->GetStr("ErrorMsg"))
		errorInfo.ErrorMsg = responseUnPacker->GetStr("ErrorMsg");
	return errorInfo;
}

CErrorInfo ufx::CallService(CConnectionInterface* connection, int functionNo, IF2Packer* requestPacker, IF2UnPacker** responseUnPacker)
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
			//应答包一般包含两个数据集，
			//第一个数据集是头部信息，包含有ErrorCode和ErrorMsg等信息
			//第二个数据集则包含具体的业务数据
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

void ufx::ShowPacket(IF2UnPacker* unPacker, string PacketType)
{
	int i = 0, t = 0, j = 0, k = 0;
	string dataset_count = "", col_name = "", one_row = "";
	for (i = 1; i < unPacker->GetDatasetCount(); ++i)
	{
		dataset_count += to_string(i);
		// 设置当前结果集
		unPacker->SetCurrentDatasetByIndex(i);

		// 打印字段
		for (t = 0; t < unPacker->GetColCount(); ++t)
		{
			col_name += unPacker->GetColName(t);
			col_name += "@";
		}
		if (col_name != "")
			print_data(col_name, "col_name");
		print_data(dataset_count, "dataset_count");
		// 打印所有记录
		for (j = 0; j < (int)unPacker->GetRowCount(); ++j)
		{
			one_row = "";
			// 打印每条记录
			for (k = 0; k < unPacker->GetColCount(); ++k)
			{
				switch (unPacker->GetColType(k))
				{
				case 'I':
					one_row += to_string(unPacker->GetIntByIndex(k)) + "@";
					break;

				case 'C':
					one_row += to_string(unPacker->GetCharByIndex(k)) + "@";
					break;

				case 'S':
					one_row += unPacker->GetStrByIndex(k);
					one_row += "\t";
					break;

				case 'F':
					one_row += to_string(unPacker->GetDoubleByIndex(k)) + "@";
					break;

				case 'R':
				{
					int nLength = 0;
					void *lpData = unPacker->GetRawByIndex(k, &nLength);

					// 对2进制数据进行处理
					cout << lpData << endl;
					break;
				}
				default:
					// 未知数据类型
					cerr << "未知数据类型" << "@";
					break;
				}
			}
			PrintData(one_row, "data");
			unPacker->Next();
		}
	}
}

CErrorInfo ufx::Connect(const char* serverAddr, CConnectionInterface** connection)
{
	CErrorInfo errorInfo;
	//创建T2SDK配置对象，并设置UFX服务器地址以及License文件
	CConfigInterface * config = NewConfig();
	config->AddRef();
	config->Load("t2sdk.ini");

	//创建连接对象，并连接UFX服务器
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

	//连接UFX服务器，参数3000为超时参数，单位毫秒
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

CErrorInfo ufx::Login(CConnectionInterface* connection, const char* operatorNo, const char* password, string& userToken)
{
	IF2Packer* lpRequestPacker = MakeLoginPacker(operatorNo, password);
	IF2UnPacker* lpUnPacker;
	//登录功能号：10001
	CErrorInfo errorInfo = CallService(connection, 10001, lpRequestPacker, &lpUnPacker);
	if (errorInfo.ErrorCode == 0)
	{
		errorInfo = GetUserToken(lpUnPacker, userToken);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

CErrorInfo ufx::GetUserToken(IF2UnPacker* responseUnPacker, string& userToken)
{
	CErrorInfo errorInfo;
	if (responseUnPacker->FindColIndex("user_token") >= 0)
	{
		userToken = responseUnPacker->GetStr("user_token");
	}
	else
	{
		errorInfo.ErrorCode = -100;
		errorInfo.ErrorMsg = "user_token字段在应答包中不存在";
	}
	return errorInfo;
}

struct ThreadFuncParam
{
	CConnectionInterface* connection;
	string userToken;
};

void ufx::HeartBeatThreadFunc(void* lp)
{
	ThreadFuncParam* param = (ThreadFuncParam*)lp;
	CConnectionInterface* connection = param->connection;
	IF2Packer* lpRequestPacker = MakeHeartBeatPacker(param->userToken.c_str());
	IF2UnPacker* lpUnPacker;
	while (true)
	{
		//心跳功能号：10000
		CallService(connection, 10000, lpRequestPacker, &lpUnPacker);
		Sleep(1000);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	delete param;
}

void ufx::HeartBeat(CConnectionInterface* connection, const char* userToken)
{
	ThreadFuncParam* param = new ThreadFuncParam();
	param->connection = connection;
	param->userToken = userToken;
	_beginthread(HeartBeatThreadFunc, 0, param);
}

void ufx::ReleaseConnection()
{
	if (connection != NULL)
	{
		connection->Release();
		connection = NULL;
		this->userToken = "";
	}
}

// public

CErrorInfo ufx::Login(LoginInfo* loguser)
{
	CErrorInfo errorInfo;

	errorInfo = this->Connect(loguser->serverAddr.c_str(), &connection);
	if (errorInfo.ErrorCode != 0)
	{
		cout << "Error:" << errorInfo.ErrorMsg << endl << errorInfo.ErrorCode;
		getchar();
		return errorInfo;
	}
	else
	{
		cout << "Connect Success." << endl;
	}

	errorInfo = this->Login(connection, loguser->operatorNo.c_str(), loguser->password.c_str(), userToken);
	if (errorInfo.ErrorCode != 0)
	{
		cout << "登录失败。错误信息为:" << errorInfo.ErrorMsg << endl;
		this->ReleaseConnection();
		getchar();
		return errorInfo;
	}
	else
	{
		cout << "登录成功。userToken=" << userToken << endl;
	}

	this->HeartBeat(connection, userToken.c_str());

	return errorInfo;
}

CErrorInfo ufx::QueryCombi()
{
	IF2Packer* lpRequestPacker = MakeCombiQuery(userToken.c_str());
	IF2UnPacker* responseUnPacker = NULL;
	//组合查询功能号：30003
	CErrorInfo errorInfo = CallService(connection, 30003, lpRequestPacker, &responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	ShowPacket(responseUnPacker, "QueryCombi");
	return errorInfo;
}

CErrorInfo ufx::QueryEntrusts(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryEntrustsPacker(userToken, accountCode, combiNo, entrustNo);
	//委托查询功能号：32001
	CErrorInfo errorInfo = CallService(connection, 32001, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

CErrorInfo ufx::QueryDeals(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryDealsPacker(userToken, accountCode, combiNo, entrustNo);

	//期货查询功能号：33003
	CErrorInfo errorInfo = CallService(connection, 33003, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

CErrorInfo ufx::QueryAccount(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryAccountPacker(userToken, accountCode, combiNo);
	//委托查询功能号：34001
	CErrorInfo errorInfo = CallService(connection, 34001, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

CErrorInfo ufx::QueryCombiStock(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryCombiStockPacker(userToken, accountCode, combiNo, marketNo, stockCode);
	//委托查询功能号：34001
	CErrorInfo errorInfo = CallService(connection, 34001, lpRequestPacker, responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

/*
** CCallback
**/

unsigned long CCallback::QueryInterface(const char *iid, IKnown **ppv)
{
	return 0;
}

unsigned long CCallback::AddRef()
{
	return 0;
}

unsigned long CCallback::Release()
{
	return 0;
}

void CCallback::OnConnect(CConnectionInterface *lpConnection)
{
	print_data("CCallback::OnConnect");
}

void CCallback::OnSafeConnect(CConnectionInterface *lpConnection)
{
	print_data("CCallback::OnSafeConnect");
}

void CCallback::OnRegister(CConnectionInterface *lpConnection)
{
	print_data("CCallback::OnRegister");
}

void CCallback::OnClose(CConnectionInterface *lpConnection)
{
	print_data("CCallback::OnClose");
}

void CCallback::OnSent(CConnectionInterface *lpConnection, int hSend, void *reserved1, void *reserved2, int nQueuingData)
{

}

void CCallback::OnReceivedBiz(CConnectionInterface *lpConnection, int hSend, const void *lpUnpackerOrStr, int nResult)
{

}
void CCallback::OnReceivedBizEx(CConnectionInterface *lpConnection, int hSend, LPRET_DATA lpRetData, const void *lpUnpackerOrStr, int nResult)
{

}
void CCallback::OnReceivedBizMsg(CConnectionInterface *lpConnection, int hSend, IBizMessage* lpMsg)
{

}
void CCallback::Reserved1(void *a, void *b, void *c, void *d)
{
}
void CCallback::Reserved2(void *a, void *b, void *c, void *d)
{
}
int  CCallback::Reserved3()
{
	return 0;
}
void CCallback::Reserved4()
{
}
void CCallback::Reserved5()
{
}
void CCallback::Reserved6()
{
}
void CCallback::Reserved7()
{
}