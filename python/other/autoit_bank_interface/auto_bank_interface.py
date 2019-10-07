# utf-8

import uiautomation as auto
import subprocess
import os
import time
import psutil

auto.SetGlobalSearchTimeout(15)


class AutoRobot:
    def __init__(self, log):
        self.log = log
        self.root_list = None

    def __check_process_exists(self, process_name=''):
        if process_name == '':
            return False

        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                self.log.debug('Process [{0}] is found!'.format(process_name))
                return True
        self.log.debug('Process [{0}] is not found!'.format(process_name))
        return False

    def start_bank_interface(self, path, password):
        exe_name = 'BiSafe.exe'
        if not self.__check_process_exists(exe_name):
            subprocess.Popen(os.path.join(path, exe_name))
            time.sleep(3)
        run_window = auto.WindowControl(searchDepth=1, Name='Bisafe')
        if run_window is not None:
            run_window.SetTopmost(True)
            service_name1 = r'NC安全HTTP服务'
            self.log.debug('get_status_and_start ' + service_name1)
            self.get_status_and_start(run_window=run_window, name=service_name1, password=password)
            service_name2 = r'NC安全无协议服务'
            self.log.debug('get_status_and_start ' + service_name2)
            self.get_status_and_start(run_window=run_window, name=service_name2, password=password)
            service_name3 = r'NC签名服务'
            self.log.debug('get_status_and_start ' + service_name3)
            self.get_status_and_start(run_window=run_window, name=service_name3, password=password)

            self.log.info('Start {0}'.format(exe_name))
            run_window.SetTopmost(False)
        else:
            self.log.error('Cannot find {0} on windows!'.format(exe_name))

    def get_status_and_start(self, run_window=None, name='', password=''):
        if run_window is None or name == '':
            return
        list_item = run_window.ListItemControl(searchDepth=4, Name=name)
        status_text = list_item.TextControl(searchDepth=5, foundIndex=3)
        self.log.debug('service {0} status {1}'.format(name, status_text.Name))
        if status_text.Name == r'停止':
            list_item.Click()
            time.sleep(1)
            tool_bar = run_window.ToolBarControl(searchDepth=3, ClassName='ToolbarWindow32')
            run_button = tool_bar.ButtonControl(searchDepth=4, foundIndex=1)
            run_button.Click()
            time.sleep(1)
            if password != '':
                self.log.debug('service {0} start with password'.format(name))
                self.send_key_in_new_window(keys=password)
                time.sleep(1)
            self.log.info('service {0} start'.format(name))

    def send_key_in_new_window(self, keys=''):
        new_window = auto.WindowControl(searchDepth=2, Name=r'口令')
        if new_window is not None:
            new_window.SetTopmost(True)
            input_edit = new_window.EditControl(searchDepth=3)
            input_edit.SendKeys(keys)
            ok_button = new_window.ButtonControl(searchDepth=3, Name=r'确定')
            ok_button.Click()
            time.sleep(1)
