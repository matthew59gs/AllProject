#include "pch.h"
#include "DataSaver.h"
#include <process.h>
#include <Windows.h>
#include <iostream>
#include <fstream>
#include <queue>

using namespace std;

DataSaver::DataSaver()
{
	sSavePath = "";
	ThreadFuncParam2* param = new ThreadFuncParam2();
	param->filepath = sSavePath;
	param->q = &this->s_info;
	_beginthread(Save2Local, 0, param);
}

DataSaver::~DataSaver() {}

void DataSaver::Save2Local(void* lp)
{
	ThreadFuncParam2* param = (ThreadFuncParam2*)lp;
	queue<string> *q = param->q;
	string filepath = param->filepath;
	ofstream output;
	output.open(filepath.c_str(), ios::app);
	if (!output)
	{
		cerr << "Open file " << filepath << " fail!" << endl;
		return;
	}
	while (true)
	{
		string s_data = "";
		while (!q->empty())
		{
			s_data += q->front() + '\n';
			q->pop();
		}
		if (s_data != "")
			output << s_data;
		Sleep(1000);
	}
	output.close();
}

bool DataSaver::SaveRecord(string in_s)
{
	s_info.push(in_s);
	return true;
}
