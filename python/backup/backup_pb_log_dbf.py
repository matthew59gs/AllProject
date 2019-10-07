#coding = UTF-8
import time
import os
import re
import sys
sys.path.append("..\\..\\public\\python")
import dunhe_public

HS_log_file_list = ["CC_#LOCAL#_#D1#.log",
                    "CPXX_#D1#.log",
                    "DYZJ_#D1#.log",
                    "hqh5api_#D2#.log",
                    "lic#D2#.log",
                    "MemData_#D2#.log",
                    "NetRate_#D2#.log",
                    "NetSpeed_#D2#.log",
                    "pbrc_#D2#.log",
                    "rcmsgclient_#D2#.log",
                    "RiskCtrl_#D1#.log",
                    "Subscribe_#D2#.log",
                    "t2sdk.log",
                    "Tentrusts_#D1#.log",
                    "Trealdeal_#D1#.log",
                    "UsedMemory_#D2#.log",
                    "wtuxws_#D2#.log",
                    "ZHCC_#D1#.log",
                    "ZJ_#LOCAL#_#D1#.log"
                    ]
HS_log_file_list2 = ['history(\d)+_#D2#.xml']
HS_DBF_list = ['XHPT_CD#D1#.dbf',
               'XHPT_CJCX#D1#.dbf',
               'XHPT_WT#D1#.dbf',
               'XHPT_WTCX#D1#.dbf',
               'XHPT_WTMX#D1#.dbf']


class HS_pb_backup:
    def __init__(self, log, local_str="", date="", log_path="", dbf_path=""):
        self.log = log
        self.log_path = log_path
        self.dbf_path = dbf_path
        self.target_log_list = []
        self.target_log_list2 = []
        self.target_DBF_list = []
        if date == "":
            self.date = time.strftime('%Y%m%d')
        else:
            self.date = date
        self.__set_date(self.date)
        self.__set_local_str(local_str=local_str)

    def __set_local_str(self, local_str=""):
        if local_str != "":
            for filename in self.target_log_list:
                if filename.find('#LOCAL#') >= 0:
                    new_filename = filename.replace('#LOCAL#', local_str)
                    self.target_log_list.remove(filename)
                    self.target_log_list.append(new_filename)

    def __date_replace(self, date1, date2, from_list, to_list):
        for filename in from_list:
            if filename.find('#D1#') >= 0:
                new_filename = filename.replace('#D1#', date1)
            elif filename.find('#D2#') >= 0:
                new_filename = filename.replace('#D2#', date2)
            else:
                new_filename = filename
            to_list.append(new_filename)

    def __set_date(self, date=""):
        if date == "":
            date1 = time.strftime('%Y%m%d')
        else:
            date1 = date
        date2 = date1[0:4] + '-' + date1[4:6] + '-' + date1[-2:]
        self.log.debug("date format1 {0}, format2 {1}".format(date1, date2))
        self.__date_replace(date1, date2, HS_log_file_list, self.target_log_list)
        self.__date_replace(date1, date2, HS_log_file_list2, self.target_log_list2)
        self.__date_replace(date1, date2, HS_DBF_list, self.target_DBF_list)

    def __backup_file(self, path="", type=""):
        if type == "log":
            if path == "":
                if self.log_path == "":
                    return
                else:
                    path = self.log_path
        elif type == "dbf":
            if path == "":
                if self.dbf_path == "":
                    return
                else:
                    path = self.dbf_path
        else:
            return

        target_dir = os.path.join(path, self.date)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        allfiles = os.listdir(path)
        target_list = []
        for file in allfiles:
            if type == "log":
                target_list = self.target_log_list
            elif type == "dbf":
                target_list = self.target_DBF_list
            if file in target_list:
                self.log.debug("Backup file {0} to {1}".format(
                    os.path.join(path, file), os.path.join(target_dir, file)))
                try:
                    dunhe_public.safe_move_file(src_dir=path, src_filename=file,
                                                target_dir=target_dir, target_filename=file)
                except Exception as e:
                    self.log.error('move_file_error:{0}'.format(e))
            # 一般文件名队列对不上的，如果是log形式，还需要和正则的list匹配一遍
            elif type == "log":
                for rule in self.target_log_list2:
                    match = re.search(rule, file)
                    if match:
                        self.log.debug("Backup file {0} to {1}".format(
                            os.path.join(path, file), os.path.join(target_dir, file)))
                        try:
                            dunhe_public.safe_move_file(src_dir=path, src_filename=file,
                                                        target_dir=target_dir, target_filename=file)
                        except Exception as e:
                            self.log.error('move_file_error:{0}'.format(e))
        return True

    def backup_log(self, path=""):
        return self.__backup_file(path=path, type="log")

    def backup_dbf(self, path=""):
        return self.__backup_file(path=path, type="dbf")


class XT_pb_backup:
    def __init__(self, log, date=""):
        self.log = log
        self.log_path = ""
        if date == "":
            self.date = time.strftime('%Y%m%d')
        else:
            self.date = date

    def backup_log(self, path):
        if path == "":
            if self.log_path == "":
                return
            else:
                path = self.log_path
        target_dir = os.path.join(path, self.date)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        allfiles = os.listdir(path)
        for file in allfiles:
            if os.path.isfile(os.path.join(path, file)):
                new_file = self.date + "_" + file
                self.log.debug("Backup file {0} to {1}".format(
                    os.path.join(path, file), os.path.join(target_dir, new_file)))
                try:
                    dunhe_public.safe_move_file(path, file, target_dir, new_file)
                except Exception as e:
                    self.log.error('move_file_error:{0}'.format(e))
            else:
                # self.log.debug("dir name is {0}".format(file))
                date_in_filename = dunhe_public.GetDateByString(file)
                # self.log.debug("get datetime from name, result {0}".format(date_in_filename))
                if date_in_filename is None:
                    all_sub_files = os.listdir(os.path.join(path, file))
                    for sub_file in all_sub_files:
                        if os.path.isfile(os.path.join(path, file, sub_file)):
                            new_file = self.date + "_" + sub_file
                            self.log.debug("Backup file {0} to {1}".format(
                                os.path.join(path, file, sub_file), os.path.join(target_dir, new_file)))
                            try:
                                dunhe_public.safe_move_file(os.path.join(path, file), sub_file, target_dir, new_file)
                            except Exception as e:
                                self.log.error('move_file_error:{0}'.format(e))
