#pragma once

#include <string>
#include <list>
#include "DataSaver.h"
#include "ufx.h"

using namespace std;

struct CombiInfo
{
	string fund;
	string account;
	string combi;
};

class Manager
{
public:
	Manager();
	~Manager();
	bool set_config();
	void print_data(string sData, string sType = "data");

	bool get_all_combi();
	bool get_account_asset(string asset);
	bool get_combi_holding(string combi);
	bool get_today_entrust(CombiInfo combi);
	bool get_today_deal(CombiInfo combi);
	bool subscribe_entrust();
	bool subscrbie_deal();

	bool get_his_account_asset(string asset, int date);
	bool get_his_combi_holding(string asset, int date);
	bool get_his_entrust(CombiInfo combi, int date);
	bool get_his_deal(CombiInfo combi, int date);
private:
	list<CombiInfo> combi_list;
	int date;
	ufx *conn;

	string asset_save_path;
	DataSaver *asset_value;

	string holding_save_path;
	DataSaver *holding;

	string entrust_save_path;
	DataSaver *entrust;

	string deal_save_path;
	DataSaver *deal;
};


int get_date_today();