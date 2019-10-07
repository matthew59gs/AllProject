#pragma once

#include <string>
#include <queue>

using namespace std;

struct ThreadFuncParam2
{
	queue<string> *q;
	string filepath;
};

class DataSaver
{
public:
	DataSaver();
	~DataSaver();

	bool SaveRecord(string in_s);
	void static Save2Local(void* lp);

	string sSavePath;

private:
	queue<string> s_info;
};

