#pragma once
#include <string>
#include "t2sdk_interface.h"
#include "Manager.h"
using namespace std;

class CErrorInfo
{
public:
	CErrorInfo() : ErrorCode(0), ErrorMsg("") {}
	int				ErrorCode;
	string			ErrorMsg;
};

class LoginInfo
{
public:
	LoginInfo() : serverAddr(""), operatorNo(""), password("") {}
	string serverAddr;	//UFX服务器地址
	string operatorNo;	//操作员
	string password;	//操作员密码
};

class ufx
{
public:
	ufx() : connection(NULL), userToken("") {}
	~ufx();

	void		ShowPacket(IF2UnPacker* unPacker, string PacketType);
	friend	void	Manager::print_data(string sData, string sType = "data");
	CErrorInfo	Login(LoginInfo* loguser);
	CErrorInfo	QueryCombi();
	CErrorInfo	QueryEntrusts(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker);
	CErrorInfo	QueryDeals(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, int entrustNo, IF2UnPacker** responseUnPacker);
	CErrorInfo	QueryAccount(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, IF2UnPacker** responseUnPacker);
	CErrorInfo	QueryCombiStock(CConnectionInterface* connection, const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode, IF2UnPacker** responseUnPacker);
	

private:
	IF2Packer			*MakeLoginPacker(const char* operatorNo, const char* password);
	IF2Packer	static	*MakeHeartBeatPacker(const char* userToken);
	CErrorInfo	static	CallService(CConnectionInterface* connection, int functionNo, IF2Packer* requestPacker, IF2UnPacker** responseUnPacker);
	CErrorInfo	static	GetErrorInfo(IF2UnPacker* responseUnPacker);
	CErrorInfo			GetUserToken(IF2UnPacker* responseUnPacker, string& userToken);
	void static			HeartBeatThreadFunc(void* lp);
	void				HeartBeat(CConnectionInterface* connection, const char* userToken);
	CErrorInfo			Connect(const char* serverAddr, CConnectionInterface** connection);
	CErrorInfo			Login(CConnectionInterface* connection, const char* operatorNo, const char* password, string& userToken);
	void				ReleaseConnection();

	IF2Packer*	MakeCombiQuery(const char* userToken);
	IF2Packer*	MakeQueryEntrustsPacker(const char* userToken, const char* accountCode, const char* combiNo, int entrustNo);
	IF2Packer*	MakeQueryDealsPacker(const char* userToken, const char* accountCode, const char* combiNo, int entrustNo);
	IF2Packer*	MakeQueryAccountPacker(const char* userToken, const char* accountCode, const char* combiNo);
	IF2Packer*	MakeQueryCombiStockPacker(const char* userToken, const char* accountCode, const char* combiNo, const char* marketNo, const char* stockCode);

	CConnectionInterface* connection;
	string userToken;
};

class CCallback : public CCallbackInterface
{
public:
	unsigned long  FUNCTION_CALL_MODE QueryInterface(const char *iid, IKnown **ppv);
	unsigned long  FUNCTION_CALL_MODE AddRef();
	unsigned long  FUNCTION_CALL_MODE Release();
	void FUNCTION_CALL_MODE OnConnect(CConnectionInterface *lpConnection);
	void FUNCTION_CALL_MODE OnSafeConnect(CConnectionInterface *lpConnection);
	void FUNCTION_CALL_MODE OnRegister(CConnectionInterface *lpConnection);
	void FUNCTION_CALL_MODE OnClose(CConnectionInterface *lpConnection);
	void FUNCTION_CALL_MODE OnSent(CConnectionInterface *lpConnection, int hSend, void *reserved1, void *reserved2, int nQueuingData);
	void FUNCTION_CALL_MODE Reserved1(void *a, void *b, void *c, void *d);
	void FUNCTION_CALL_MODE Reserved2(void *a, void *b, void *c, void *d);
	int  FUNCTION_CALL_MODE Reserved3();
	void FUNCTION_CALL_MODE Reserved4();
	void FUNCTION_CALL_MODE Reserved5();
	void FUNCTION_CALL_MODE Reserved6();
	void FUNCTION_CALL_MODE Reserved7();
	void FUNCTION_CALL_MODE OnReceivedBiz(CConnectionInterface *lpConnection, int hSend, const void *lpUnPackerOrStr, int nResult);
	void FUNCTION_CALL_MODE OnReceivedBizEx(CConnectionInterface *lpConnection, int hSend, LPRET_DATA lpRetData, const void *lpUnpackerOrStr, int nResult);
	void FUNCTION_CALL_MODE OnReceivedBizMsg(CConnectionInterface *lpConnection, int hSend, IBizMessage* lpMsg);

	friend void Manager::print_data(string sData, string sType = "data");
};