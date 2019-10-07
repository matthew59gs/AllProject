#include "pch.h"
#include "Manager.h"
#include <iostream>
#include <ctime>

using namespace std;

Manager::Manager()
{
}


Manager::~Manager()
{
}

void Manager::print_data(string sData, string sType = "data")
{
	if (sType == "col_name")
	{
		cout << "ColumnName:" << endl;
		cout << sData << endl;
	}
	else if (sType == "dataset_count")
	{
		cout << "DataSet[" << sData << "]" << endl;
	}
	else if (sType == "data")
	{
		cout << sData << endl;
	}
}

int get_date_today()
{
	time_t now = time(0);
	tm* now_t = localtime(&now);
	return now_t->tm_year * 10000 + now_t->tm_mon * 100 + now_t->tm_mday;
}