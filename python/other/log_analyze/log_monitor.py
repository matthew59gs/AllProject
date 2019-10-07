#!/usr/bin/env python

import time
import re
import os


def search_text(log=None, src_file='', target_list=[], target_file=''):
    if src_file == '' or len(target_list) == 0:
        return False
    log.info('In log {0} to find text {1}'.format(src_file, target_list))
    fr = open(src_file, 'r')
    if target_file == '':
        target_file = os.path.join(os.path.dirname(src_file), 'result.log')
    fw = open(target_file, 'a')
    content = fr.read()
    for target_text in target_list:
        match = re.search(target_text, content)
        if match:
            fw.writelines(match.group())
            fw.write('\n')
            log.info('Find target text {0}'.format(match.group()))
    fr.close()
    fw.close()
    return True


class LogMonitor:
    def __init__(self, log):
        self.log = log
        self.src_path = ''
        self.tar_path = ''
        self.date = ''

    def set_log_path(self, path):
        self.src_path = path

    def set_result_path(self, path):
        self.tar_path = path

    def set_date(self, date):
        if date == '0':
            self.date = time.strftime('%Y-%m-%d')
        else:
            re_str = r'\d{8}'
            match = re.search(re_str, date)
            if match:
                self.date = date[0:4] + '-' + date[4:6] + '-' + date[-2:]
            else:
                self.date = time.strftime('%Y-%m-%d')


class OplusLogMonitor(LogMonitor):
    def find_result(self):
        if self.tar_path == '':
            self.tar_path = self.src_path

        LOG_NAME = r'\d{9}-ULOG-#D#.log'
        TARGET_TEXT_LIST = [r'[菜单|PB文件导出](\S+)提示：委托导出任务（配置号：(\d+,?)+）启动成功']
        RESULT_FILE_NAME = 'monitor_result_#D#.log'.replace('#D#', self.date)
        re_str = LOG_NAME.replace('#D#', self.date)
        file_list = os.listdir(self.src_path)
        for filename in file_list:
            match = re.search(re_str, filename)
            if match:
                return search_text(log=self.log,
                                   src_file=os.path.join(self.src_path, filename),
                                   target_list=TARGET_TEXT_LIST,
                                   target_file=os.path.join(self.tar_path, RESULT_FILE_NAME))
        return False


class PBLogMonitor(LogMonitor):
    def find_result(self):
        if self.tar_path == '':
            self.tar_path = self.src_path

        LOG_NAME = 'pbrc_#D#.log'
        TARGET_TEXT_LIST = [r'文件监控已开始！',
                            r'完成委托查询数据加载，总计 (\d+) 笔',
                            r'完成委托查询数据同步，新增 (\d+) 笔，修改 (\d+) 笔',
                            r'完成委托数据同步，更新 (\d+) 笔',
                            r'完成成交查询数据加载，总计 (\d+) 笔',
                            r'完成成交查询数据同步，新增 (\d+) 笔']
        RESULT_FILE_NAME = 'monitor_result_#D#.log'.replace('#D#', self.date)
        re_str = LOG_NAME.replace('#D#', self.date)
        file_list = os.listdir(self.src_path)
        for filename in file_list:
            match = re.search(re_str, filename)
            if match:
                return search_text(log=self.log,
                                   src_file=os.path.join(self.src_path, filename),
                                   target_list=TARGET_TEXT_LIST,
                                   target_file=os.path.join(self.tar_path, RESULT_FILE_NAME))
        return False
