/** @file
* ��ʾT2_SDK���д�����������հ������
* @author  T2С��
* @author  �������ӹɷ����޹�˾
* @version 1.0
* @date    20090327
*/
#include <Include/t2sdk_interface.h>
#include <map>
using namespace std;

map<int, CSubscribeParamInterface*> g_allSubscribeParam;
CConnectionInterface *g_lpConnection = NULL;

void PrintUnPack(IF2UnPacker* lpUnPack)
{
	printf("��¼������           %d\n",lpUnPack->GetRowCount());
	printf("��������			 %d\n",lpUnPack->GetColCount());
	while (!lpUnPack->IsEOF())
	{
		for (int i=0;i<lpUnPack->GetColCount();i++)
		{
			char* colName = (char*)lpUnPack->GetColName(i);
			char colType = lpUnPack->GetColType(i);
			if (colType!='R')
			{
				char* colValue = (char*)lpUnPack->GetStrByIndex(i);
				printf("%s:			[%s]\n",colName,colValue);
			}
			else
			{
				int colLength = 0;
				char* colValue = (char*)lpUnPack->GetRawByIndex(i,&colLength);
				printf("%s:			[%s](%d)\n",colName,colValue,colLength);
			}
		}
		lpUnPack->Next();
	}

}

void PrintSub(int subIndex,LPSUBSCRIBE_RECVDATA lpRecvData)
{
	map<int, CSubscribeParamInterface*>::iterator itr = g_allSubscribeParam.find(subIndex);
	if(itr==g_allSubscribeParam.end())
	{
		printf("û�����������\n");
		return ;
	}
	CSubscribeParamInterface* lpSubParam = (*itr).second;

	printf("----------�������-------\n");
	printf("�������֣�           %s\n",lpSubParam->GetTopicName());
	printf("�������ݳ��ȣ�       %d\n",lpRecvData->iAppDataLen);
	if (lpRecvData->iAppDataLen>0)
	{
		printf("�������ݣ�           %s\n",lpRecvData->lpAppData);
	}
	printf("�����ֶβ��֣�\n");
	if(lpRecvData->iFilterDataLen>0)
	{
		IF2UnPacker* lpUnpack = NewUnPacker(lpRecvData->lpFilterData,lpRecvData->iFilterDataLen);
		lpUnpack->AddRef();
		PrintUnPack(lpUnpack);
		lpUnpack->Release();
	}

	printf("---------------------------\n");	

}


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

};
//���¸��ص�������ʵ�ֽ���Ϊ��ʾʹ��
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
	puts("CCallback::OnConnect");
}

void CCallback::OnSafeConnect(CConnectionInterface *lpConnection)
{
	puts("CCallback::OnSafeConnect");
}

void CCallback::OnRegister(CConnectionInterface *lpConnection)
{
	puts("CCallback::OnRegister");
}

void CCallback::OnClose(CConnectionInterface *lpConnection)
{
	puts("CCallback::OnClose");
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
class CSubCallback : public CSubCallbackInterface
{
	unsigned long  FUNCTION_CALL_MODE QueryInterface(const char *iid, IKnown **ppv)
	{
		return 0;
	}
	unsigned long  FUNCTION_CALL_MODE AddRef()
	{
		return 0;
	}
	unsigned long  FUNCTION_CALL_MODE Release()
	{
		return 0;
	}

	void FUNCTION_CALL_MODE OnReceived(CSubscribeInterface *lpSub,int subscribeIndex, const void *lpData, int nLength,LPSUBSCRIBE_RECVDATA lpRecvData);
	void FUNCTION_CALL_MODE OnRecvTickMsg(CSubscribeInterface *lpSub,int subscribeIndex,const char* TickMsgInfo);
};





void CSubCallback::OnReceived(CSubscribeInterface *lpSub,int subscribeIndex, const void *lpData, int nLength,
	LPSUBSCRIBE_RECVDATA lpRecvData)
{
	printf("***************************\n");
	PrintSub(subscribeIndex,lpRecvData);
	IF2UnPacker* lpUnPack = NewUnPacker((void*)lpData,nLength);
	if (lpUnPack)
	{
		lpUnPack->AddRef();
		PrintUnPack(lpUnPack);
		lpUnPack->Release();
	}
	printf("***************************\n");
}
void CSubCallback::OnRecvTickMsg(CSubscribeInterface *lpSub,int subscribeIndex,const char* TickMsgInfo)
{

}


int main()
{
	//ͨ��T2SDK����������������ȡһ���µ�CConfig����ָ��
	//�˶����ڴ������Ӷ���ʱ�����ݣ��������������������Ӷ���ĸ������ԣ����������IP��ַ����ȫģʽ�ȣ�
	//ֵ��ע����ǣ��������ö�������������Ϣʱ��������Ϣ�ȿ��Դ�ini�ļ������룬
	//Ҳ�����ڳ���������趨��������2�ߵĻ�ϣ������ͬһ���������費ͬ��ֵ���������һ������Ϊ׼
	CConfigInterface * lpConfig = NewConfig();
	lpConfig->AddRef();
	lpConfig->Load("subscriber.ini");
	//�����Ҫʹ�÷������Ĺ��ܣ�������������mc��ǩ�����client_name������ļ��������ˣ�����Ҫ��������������
	//lpConfig->SetString("mc","client_name","xuxp");

	//ͨ��T2SDK����������������ȡһ���µ�CConnection����ָ��
	g_lpConnection = NewConnection(lpConfig);
	g_lpConnection->AddRef();

	//�����Զ�����CCallback�Ķ����ڴ�������ʱ�贫�ݴ˶����뿴������룩
	CCallback callback;

	int ret = 0;

	//��ʼ�����Ӷ��󣬷���0��ʾ��ʼ���ɹ���ע���ʱ��û��ʼ���ӷ�����
	if (0 == (ret = g_lpConnection->Create2BizMsg(&callback)))
	{
		//��ʽ��ʼ���ӣ�����1000Ϊ��ʱ��������λ��ms
		if (ret = g_lpConnection->Connect(1000))
		{
			puts(g_lpConnection->GetErrorMsg(ret));
		}
		else
		{
			CSubCallback subscriberCallback;
			char* bizName = (char*)lpConfig->GetString("subcribe","biz_name","");
			//�����Ҫʹ�÷������Ĺ��ܣ�������������mc��ǩ�����client_name��
			CSubscribeInterface* lpSub = g_lpConnection->NewSubscriber(&subscriberCallback,bizName,5000);
			if (!lpSub)
			{
				printf("NewSubscribe Error: %s\n",g_lpConnection->GetMCLastError());
				return -1;
			}
			lpSub->AddRef();


			//���Ĳ�����ȡ
			CSubscribeParamInterface* lpSubscribeParam = NewSubscribeParam();
			lpSubscribeParam->AddRef();
			char* topicName = (char*)lpConfig->GetString("subcribe","topic_name","");//��������
			lpSubscribeParam->SetTopicName(topicName);
			char* isFromNow = (char*)lpConfig->GetString("subcribe","is_rebulid","");//�Ƿ�ȱ
			if (strcmp(isFromNow,"true")==0)
			{
				lpSubscribeParam->SetFromNow(true);
			}
			else
			{
				lpSubscribeParam->SetFromNow(false);
			}

			char* isReplace = (char*)lpConfig->GetString("subcribe","is_replace","");//�Ƿ񸲸�
			if (strcmp(isReplace,"true")==0)
			{
				lpSubscribeParam->SetReplace(true);
			}
			else
			{
				lpSubscribeParam->SetReplace(false);
			}

			char* lpApp = "xuxinpeng";
			lpSubscribeParam->SetAppData(lpApp,9);//���Ӹ�������

			//���ӹ����ֶ�
			int nCount = lpConfig->GetInt("subcribe","filter_count",0);
			for (int i=1;i<=nCount;i++)
			{
				char lName[128]={0};
				sprintf(lName,"filter_name%d",i);
				char* filterName = (char*)lpConfig->GetString("subcribe",lName,"");
				char lValue[128]={0};
				sprintf(lValue,"filter_value%d",i);
				char* filterValue = (char*)lpConfig->GetString("subcribe",lValue,"");
				lpSubscribeParam->SetFilter(filterName,filterValue);
			}
			//���ӷ���Ƶ��
			lpSubscribeParam->SetSendInterval(lpConfig->GetInt("subcribe","send_interval",0));
			//���ӷ����ֶ�
			nCount = lpConfig->GetInt("subcribe","return_count",0);
			for (int k=1;k<=nCount;k++)
			{
				char lName[128]={0};
				sprintf(lName,"return_filed%d",k);
				char* filedName = (char*)lpConfig->GetString("subcribe",lName,"");
				lpSubscribeParam->SetReturnFiled(filedName);
			}
      
      IF2Packer* pack = NewPacker(2);
      pack->AddRef();

      //����һ��ҵ���
      pack->BeginPack();
      pack->AddField("login_operator_no");
      pack->AddField("password");
      pack->AddStr("1000");
      pack->AddStr("0");
      pack->EndPack();
      IF2UnPacker* lpBack = NULL;

			int subscribeIndex = 0;
			printf("��ʼ����\n");
			int  iRet = lpSub->SubscribeTopic(lpSubscribeParam,5000,&lpBack,pack);
			if(iRet>0)
			{
				subscribeIndex = iRet;
				printf("SubscribeTopic info:[%d] �ɹ�\n",iRet);
				g_allSubscribeParam[subscribeIndex] = lpSubscribeParam;//���浽map�У������Ժ��ȡ������
			}
			else
			{
        if(lpBack != NULL)
          PrintUnPack(lpBack);
				printf("SubscribeTopic info:[%d] %s\n",iRet,g_lpConnection->GetErrorMsg(iRet));
				return-1;
			}


			//��ӡ�Ѿ����ĵ�������Ϣ
			printf("**********************************************\n");
			IF2Packer* lpPack = NewPacker(2);
			lpPack->AddRef();
			lpSub->GetSubcribeTopic(lpPack);
			if (lpPack)
			{
				PrintUnPack(lpPack->UnPack());
			}
			lpPack->FreeMem(lpPack->GetPackBuf());
			lpPack->Release();
			printf("**********************************************\n");
			printf("���������ַ�ȡ������\n");
			getchar();


			//���ӹ����ֶ�
			iRet = lpSub->CancelSubscribeTopic(subscribeIndex);
			printf("CancelSubscribeTopic:%d %s\n",iRet,g_lpConnection->GetErrorMsg(iRet));
			printf("���������ַ��˳�\n");
			getchar();

			//�ͷŶ��Ķ�
			lpSub->Release();
			printf("�˳�\n");
		}	
	}
	else
	{
		puts(g_lpConnection->GetErrorMsg(ret));
	}

	//ͨ��getchar�����̣߳��ȴ������Ӧ�������
	getchar();

	g_lpConnection->Release();
	lpConfig->Release();
	return 0;
}