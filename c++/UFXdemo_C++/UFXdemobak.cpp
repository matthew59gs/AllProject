#include "t2sdk_interface.h"
#include <iostream>
#include <string>
#include <stdlib.h>
#include <Windows.h>
#include <process.h>
using namespace std;


class CErrorInfo
{
public:
	CErrorInfo():ErrorCode(0),ErrorMsg(""){}
	int    ErrorCode;
	string ErrorMsg;
};

void       ShowPacket(IF2UnPacker* unPacker);
CErrorInfo Connect(const char* serverAddr,CConnectionInterface** connection);
CErrorInfo Login(CConnectionInterface* connection, const char* operatorNo, const char* password, string& userToken);
CErrorInfo Entrust(CConnectionInterface* connection,const char* userToken, const char* combiNo,const char* marketNo, const char* stockCode, const char* entrustDirection, double entrustPrice, int entrustAmount,int& entrustNo);
CErrorInfo QueryEntrusts(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo,int entrustNo, IF2UnPacker** responseUnPacker);
CErrorInfo QueryDeals(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo,int entrustNo, IF2UnPacker** responseUnPacker);
CErrorInfo QueryAccount(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo, IF2UnPacker** responseUnPacker);
CErrorInfo QueryCombiStock(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo,const char* marketNo, const char* stockCode, IF2UnPacker** responseUnPacker);
void       HeartBeat(CConnectionInterface* connection,const char* userToken);

int main(int argc, char** argv)
{
	/*
	if(argc < 4)
	{
		cout << "Usage: UFXDemo serverAddr operatorNo, password, accountCode combiNo" << endl
			 << "Examples:" << endl
			 << "	UFXDemo 192.168.54.57:9012 1000 0 184693 1000005" << endl;
		getchar();
		return 0;
	}*/
 
	string serverAddr  = "115.233.212.240:20001"; //UFX服务器地址
	string operatorNo  = "000300014";               //操作员
	string password    = "dunhe@12345";                  //密码
	string accountCode = "00030001";             //账户代码
	string combiNo     = "0002";            //单元代码
	if(argc >=4)
	{
		serverAddr  = argv[1];
		accountCode = argv[2];
		combiNo     = argv[3];
	}

	string marketNo         = "1";         //交易市场
	string stockCode        = "801354";    //证券代码
	string entrustDirection = "3";         //委托方向
	double entrustPrice     = 10.10;       //委托价格
	int    entrustAmount    = 100;         //委托数量

	CErrorInfo            errorInfo;
	string                userToken;
	CConnectionInterface* connection;
	int                   entrustNo=0;
	IF2UnPacker*          responseUnPacker;

	//连接
	errorInfo = Connect(serverAddr.c_str(),&connection);
	if(errorInfo.ErrorCode != 0)
	{
		cout << "Error:" << errorInfo.ErrorMsg << endl<< errorInfo.ErrorCode;
		getchar();
		return -1;
	}
	else
	{
		cout << "Connect Success." << endl;
	}

	//登录
	errorInfo = Login(connection,operatorNo.c_str(),password.c_str(),userToken);
	if(errorInfo.ErrorCode != 0)
	{
		cout << "登录失败。错误信息为:" << errorInfo.ErrorMsg << endl;
		connection->Release();
		getchar();
		return -1;
	}
	else
	{
		cout << "登录成功。userToken=" << userToken << endl;
	}

	//心跳
	HeartBeat(connection,userToken.c_str());


	////委托
	//errorInfo = Entrust(connection,userToken.c_str(),combiNo.c_str(),marketNo.c_str(),stockCode.c_str(),entrustDirection.c_str(),entrustPrice,entrustAmount,entrustNo);
	//if(errorInfo.ErrorCode != 0)
	//{
	//	cout << "委托失败。错误信息为:" << errorInfo.ErrorMsg << endl;
	//	connection->Release();
	//	getchar();
	//	return -1;
	//}
	//else
	//{
	//	cout << "委托成功。" << endl;
	//}


	//查成交
	errorInfo = QueryDeals(connection,userToken.c_str(),accountCode.c_str(),combiNo.c_str(),entrustNo,&responseUnPacker);
	if(errorInfo.ErrorCode != 0)
	{
		cout << "查成交失败。错误信息为:" << errorInfo.ErrorMsg << endl;
		connection->Release();
		getchar();
		return -1;
	}
	else
	{
		cout << "---------Tradeinfo-----------" << endl;
		ShowPacket(responseUnPacker);
	}

	////查资金
	//errorInfo = QueryAccount(connection,userToken.c_str(),accountCode.c_str(),combiNo.c_str(),&responseUnPacker);
	//if(errorInfo.ErrorCode != 0)
	//{
	//	cout << "查资金失败。错误信息为:" << errorInfo.ErrorMsg << endl;
	//	connection->Release();
	//	getchar();
	//	return -1;
	//}
	//else
	//{
	//	cout << "---------资金信息-----------" << endl;
	//	ShowPacket(responseUnPacker);
	//}

	////查持仓
	//errorInfo = QueryCombiStock(connection,userToken.c_str(),accountCode.c_str(),combiNo.c_str(),marketNo.c_str(),stockCode.c_str(),&responseUnPacker);
	//if(errorInfo.ErrorCode != 0)
	//{
	//	cout << "查持仓失败。错误信息为:" << errorInfo.ErrorMsg << endl;
	//	connection->Release();
	//	getchar();
	//	return -1;
	//}
	//else
	//{
	//	cout << "---------持仓信息-----------" << endl;
	//	ShowPacket(responseUnPacker);
	//}
	//connection->Release();

    return 0;
}


void ShowPacket(IF2UnPacker* unPacker)
{
	int i = 0, t = 0, j = 0, k = 0;
	FILE *fp;
	fopen_s(&fp,"test.csv", "w");

	for (i = 1; i < unPacker->GetDatasetCount(); ++i)
	{
		printf("%d",i);
		// 设置当前结果集
		unPacker->SetCurrentDatasetByIndex(i);

		// 打印字段
		for (t = 0; t < unPacker->GetColCount(); ++t)
		{
			fprintf(fp,"%s,", unPacker->GetColName(t));
		}
		fprintf(fp, "\n");

		// 打印所有记录
		for (j = 0; j < (int)unPacker->GetRowCount(); ++j)
		{
			// 打印每条记录
			for (k = 0; k < unPacker->GetColCount(); ++k)
			{
				switch (unPacker->GetColType(k))
				{
				case 'I':
					fprintf(fp,"%d,", unPacker->GetIntByIndex(k));
					break;

				case 'C':
					fprintf(fp,"%c,", unPacker->GetCharByIndex(k));
					break;

				case 'S':
					fprintf(fp,"%s,", unPacker->GetStrByIndex(k));
					break;

				case 'F':
					fprintf(fp,"%f,", unPacker->GetDoubleByIndex(k));
					break;

				case 'R':
					{
						int nLength = 0;
						void *lpData = unPacker->GetRawByIndex(k, &nLength);

						// 对2进制数据进行处理
						break;
					}

				default:
					// 未知数据类型
					printf("未知数据类型。\n");
					break;
				}
			}

			fprintf(fp,"\n");
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
	if(responseUnPacker->GetStr("ErrorMsg"))
		errorInfo.ErrorMsg  = responseUnPacker->GetStr("ErrorMsg");
	return errorInfo;
}

CErrorInfo CallService(CConnectionInterface* connection,int functionNo, IF2Packer* requestPacker, IF2UnPacker** responseUnPacker)
{
	CErrorInfo errorInfo;
	int ret = connection->SendBiz(functionNo,requestPacker);
	if (ret > 0)
	{
		void* Pointer;
		ret = connection->RecvBiz(ret,&Pointer,3000);
		switch(ret)
		{
		case 0:
		case 1:
			//应答包一般包含两个数据集，
			//第一个数据集是头部信息，包含有ErrorCode和ErrorMsg等信息
			//第二个数据集则包含具体的业务数据
			(*responseUnPacker) = (IF2UnPacker*)Pointer;
			errorInfo = GetErrorInfo(*responseUnPacker);
			if((*responseUnPacker)->GetDatasetCount() > 1) (*responseUnPacker)->SetCurrentDatasetByIndex(1);
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

CErrorInfo Connect(const char* serverAddr,CConnectionInterface** connection)
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
	if( ret != 0)
	{
		errorInfo.ErrorCode = ret;
		errorInfo.ErrorMsg =  conn->GetErrorMsg(ret);
        conn->Release();
        config->Release();
		return errorInfo;
	}

	//连接UFX服务器，参数3000为超时参数，单位毫秒
	ret = conn->Connect(3000);
	if( ret != 0)
	{
		errorInfo.ErrorCode = ret;
		errorInfo.ErrorMsg =  conn->GetErrorMsg(ret);
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
	requestPacker->AddField("operator_no",     'S',16, 0);
	requestPacker->AddField("password",        'S',32, 0);
	requestPacker->AddField("mac_address",     'S',255,0);
	requestPacker->AddField("op_station",      'S',255,0);
	requestPacker->AddField("ip_address",      'S',32, 0);
	requestPacker->AddField("authorization_id",'S',64, 0);
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
	if (responseUnPacker->FindColIndex("user_token") >=0 )
	{
		userToken = responseUnPacker->GetStr("user_token");
	}
	else
	{
		errorInfo.ErrorCode = -100;
		errorInfo.ErrorMsg  = "user_token字段在应答包中不存在";
	}
	return errorInfo;
}

CErrorInfo Login(CConnectionInterface* connection, const char* operatorNo, const char* password, string& userToken)
{
	IF2Packer* lpRequestPacker = MakeLoginPacker(operatorNo,password);
	IF2UnPacker* lpUnPacker;
	//登录功能号：10001
	CErrorInfo errorInfo = CallService(connection,10001,lpRequestPacker,&lpUnPacker);
	if(errorInfo.ErrorCode == 0)
	{
		errorInfo = GetUserToken(lpUnPacker,userToken);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeEntrustPacker(const char* userToken, const char* combiNo,const char* marketNo
	, const char* stockCode, const char* entrustDirection, double entrustPrice, int entrustAmount)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token",        'S',512,0);
	requestPacker->AddField("combi_no"  ,        'S',8,0);
	requestPacker->AddField("market_no" ,        'S',3,0);
	requestPacker->AddField("stock_code",        'S',16,0);
	requestPacker->AddField("entrust_direction", 'S',1,0);
	requestPacker->AddField("price_type",        'S',1,0);
	requestPacker->AddField("entrust_price",     'F',9,3);
	requestPacker->AddField("entrust_amount",    'F',16,2);
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(combiNo);
	requestPacker->AddStr(marketNo);
	requestPacker->AddStr(stockCode);
	requestPacker->AddStr(entrustDirection);
	requestPacker->AddStr("0");                  //限价
	requestPacker->AddDouble(entrustPrice);
	requestPacker->AddDouble(entrustAmount);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo GetEntrustNo(IF2UnPacker* responseUnPacker, int& entrustNo)
{
	CErrorInfo errorInfo;
	if (responseUnPacker->FindColIndex("entrust_no") >=0 )
	{
		entrustNo = responseUnPacker->GetInt("entrust_no");
	}
	else
	{
		errorInfo.ErrorCode = -100;
		errorInfo.ErrorMsg  = "entrust_no字段在应答包中不存在";
	}
	printf("%d", entrustNo);
	return errorInfo;
}

CErrorInfo Entrust(CConnectionInterface* connection,const char* userToken, const char* combiNo,const char* marketNo, const char* stockCode, const char* entrustDirection, double entrustPrice, int entrustAmount,int& entrustNo)
{
	IF2Packer* lpRequestPacker = MakeEntrustPacker(userToken,combiNo,marketNo,stockCode,entrustDirection,entrustPrice,entrustAmount);
	IF2UnPacker* lpUnPacker;
	//登录功能号：91001
	CErrorInfo errorInfo = CallService(connection,91001,lpRequestPacker,&lpUnPacker);
	if(errorInfo.ErrorCode == 0)
	{
		errorInfo = GetEntrustNo(lpUnPacker,entrustNo);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryEntrustsPacker(const char* userToken, const char* accountCode, const char* combiNo,int entrustNo)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S',512);
	requestPacker->AddField("account_no", 'S',32);
	requestPacker->AddField("combi_no",   'S',8);
	requestPacker->AddField("entrust_no", 'I');
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->AddInt(entrustNo);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryEntrusts(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo,int entrustNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryEntrustsPacker(userToken,accountCode,combiNo,entrustNo);
	//委托查询功能号：32001
	CErrorInfo errorInfo = CallService(connection,32001,lpRequestPacker,responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryDealsPacker(const char* userToken, const char* accountCode, const char* combiNo,int entrustNo)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S',512);
	requestPacker->AddField("account_code", 'S',32);
	requestPacker->AddField("asset_no",   'S',16);
	requestPacker->AddField("entrust_no", 'I');
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->AddInt(entrustNo);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryDeals(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo,int entrustNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryDealsPacker(userToken,accountCode,combiNo,entrustNo);

	//期货查询功能号：33003
	CErrorInfo errorInfo = CallService(connection,33003,lpRequestPacker,responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryAccountPacker(const char* userToken, const char* accountCode, const char* combiNo)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S',512);
	requestPacker->AddField("account_no", 'S',32);
	requestPacker->AddField("combi_no",   'S',8);
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryAccount(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryAccountPacker(userToken,accountCode,combiNo);
	//委托查询功能号：34001
	CErrorInfo errorInfo = CallService(connection,34001,lpRequestPacker,responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeQueryCombiStockPacker(const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S',512);
	requestPacker->AddField("account_no", 'S',32);
	requestPacker->AddField("combi_no",   'S',8);
	requestPacker->AddField("market_no" , 'S',3);
	requestPacker->AddField("stock_code", 'S',16);
	requestPacker->AddStr(userToken);
	requestPacker->AddStr(accountCode);
	requestPacker->AddStr(combiNo);
	requestPacker->AddStr(marketNo);
	requestPacker->AddStr(stockCode);
	requestPacker->EndPack();
	return requestPacker;
}

CErrorInfo QueryCombiStock(CConnectionInterface* connection,const char* userToken, const char* accountCode, const char* combiNo,const char* marketNo, const char* stockCode, IF2UnPacker** responseUnPacker)
{
	IF2Packer* lpRequestPacker = MakeQueryCombiStockPacker(userToken,accountCode,combiNo,marketNo,stockCode);
	//委托查询功能号：34001
	CErrorInfo errorInfo = CallService(connection,34001,lpRequestPacker,responseUnPacker);
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	return errorInfo;
}

IF2Packer* MakeHeartBeatPacker(const char* userToken)
{
	IF2Packer* requestPacker = NewPacker(2);
	requestPacker->AddRef();
	requestPacker->BeginPack();
	requestPacker->AddField("user_token", 'S',512);
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
	while(true)
	{
		//心跳功能号：10000
		CallService(connection,10000,lpRequestPacker,&lpUnPacker);
		Sleep(1000);
	}
	lpRequestPacker->FreeMem(lpRequestPacker->GetPackBuf());
	lpRequestPacker->Release();
	delete param;
}

void HeartBeat(CConnectionInterface* connection,const char* userToken)
{
	ThreadFuncParam* param = new ThreadFuncParam();
	param->connection = connection;
	param->userToken = userToken;
	_beginthread(HeartBeatThreadFunc,0,param);
}
