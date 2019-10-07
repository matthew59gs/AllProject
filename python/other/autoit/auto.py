# utf-8
# dependency uiautomation psutil

import uiautomation as auto
import subprocess
import os
import time
import psutil
from xml.dom.minidom import parse

auto.SetGlobalSearchTimeout(15)

_EXE_TAG = 'exe'
_EXENAME_TAG = 'exename'
_PATH_TAG = 'path'
_CLASSNAME_TAG = 'ClassName'
_DEPTH_TAG = 'Depth'
_NAME_TAG='Name'
_BUTTON_TAG='button'
_BUTTONINTERVAL_TAG='buttoninterval'
_AUTOMATIONID_TAG='AutomationId'

class AutoStartExe:
    def __init__(self, logger, configpath=''):
        self.logger = logger
        self.rootlist = None
        if configpath != '':
            self.load_config(path=configpath)

    def load_config(self, path=''):
        if path == '':
            return

        self.rootlist = parse(path).documentElement
        self.logger.info('Load xml config: {0}'.format(path))

    def run_config(self, path=''):
        if path != '':
            self.load_config(path)
        else:
            if self.rootlist is None:
                self.logger.error('No config path!')
                return

        for exe in self.rootlist.getElementsByTagName(_EXE_TAG):
            self.__run_exe(exe)

    def __run_exe(self, exeXML=None):
        exename = exeXML.getElementsByTagName(_EXENAME_TAG)[0].childNodes[0].data
        path = exeXML.getElementsByTagName(_PATH_TAG)[0].childNodes[0].data
        classname = exeXML.getElementsByTagName(_CLASSNAME_TAG)[0].childNodes[0].data
        depth = int(exeXML.getElementsByTagName(_DEPTH_TAG)[0].childNodes[0].data)
        name = exeXML.getElementsByTagName(_NAME_TAG)[0].childNodes[0].data
        if not self.__check_process_exists(exename):
            subprocess.Popen(os.path.join(path, exename))
            time.sleep(5)
        foundIndex = 1
        run_window = auto.WindowControl(searchDepth=depth, foundIndex=foundIndex, ClassName=classname)
        if run_window is not None:
            if run_window.Name != name:
                self.logger.debug('Found more than one window with ClassName[{0}]'.format(classname))
                foundIndex = foundIndex + 1
                run_window = auto.WindowControl(searchDepth=depth, foundIndex=foundIndex, ClassName=classname)
            self.logger.info('Start {0}'.format(exename))
            buttons = exeXML.getElementsByTagName(_BUTTON_TAG)
            if len(buttons) > 0:
                self.__click_button(exename=exename, run_window=run_window, exeXML=exeXML)
        else:
            self.logger.error('Cannot find {0} on windows!'.format(exename))

    def __click_button(self, exename='', run_window=None, exeXML=None):
        if run_window == None or exeXML == None:
            return

        for button in exeXML.getElementsByTagName(_BUTTON_TAG) :
            buttoninterval = int(button.getElementsByTagName(_BUTTONINTERVAL_TAG)[0].childNodes[0].data)
            automationId = button.getElementsByTagName(_AUTOMATIONID_TAG)[0].childNodes[0].data
            depth = int(button.getElementsByTagName(_DEPTH_TAG)[0].childNodes[0].data)
            run_button = run_window.ButtonControl(searchDepth=depth, AutomationId=automationId)
            run_window.SetTopmost(True)
            run_button.Click()
            self.logger.info('Button[{0}] click'.format(automationId))
            try:
                run_window.SetTopmost(False)
            except Exception as e:
                self.logger.error('run_window set error: {0}'.format(e))
            time.sleep(buttoninterval)

    def start_risk_data_manager(self, path):
        exename = 'RiskDataManage.exe'
        if not self.__check_process_exists(exename):
            subprocess.Popen(os.path.join(path, exename))
            time.sleep(5)
        run_window = auto.WindowControl(searchDepth=1, AutomationId='frmMain')
        if run_window is not None:
            run_window.SetTopmost(True)
            run_button = run_window.ButtonControl(searchDepth=2, AutomationId='btnStart')
            run_button.Click()
            run_window.SetTopmost(False)
            self.logger.info('Start {0}'.format(exename))
        else:
            self.logger.error('Cannot find {0} on windows!'.format(exename))

    def stop_risk_data_manager(self):
        exename = 'RiskDataManage.exe'
        if not self.__check_process_exists(exename):
            return
        run_window = auto.WindowControl(searchDepth=1, AutomationId='frmMain')
        if run_window is not None:
            run_window.SetTopmost(True)
            close_button = run_window.ButtonControl(searchDepth=2, AutomationId='btnExit')
            close_button.Click()
            self.logger.info('Close {0}.exe'.format(exename))
        else:
            self.logger.error('Cannot find {0} on windows!'.format(exename))

    def __check_process_exists(self, process_name=''):
        if process_name == '':
            return False

        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                self.logger.debug('Process [{0}] is found!'.format(process_name))
                return True
        self.logger.debug('Process [{0}] is not found!'.format(process_name))
        return False

    def start_batch_order_tool(self, path):
        exename = 'BatchOrder.exe'
        if not self.__check_process_exists(exename):
            subprocess.Popen(os.path.join(path, exename))
            time.sleep(5)
        run_window = auto.WindowControl(searchDepth=1, ClassName='WindowsForms10.Window.8.app.0.141b42a_r14_ad1')
        if run_window is not None:
            run_window.SetTopmost(True)
            run_button = run_window.ButtonControl(searchDepth=2, AutomationId='btnRun')
            run_button.Click()
            run_window.SetTopmost(False)
            self.logger.info('Start {0}'.format(exename))
        else:
            self.logger.error('Cannot find {0} on windows!'.format(exename))

    def start_pbmonitor(self, path):
        exename = 'pbmonitor.exe'
        if not self.__check_process_exists(exename):
            subprocess.Popen(os.path.join(path, exename))
            time.sleep(5)
            if self.__check_process_exists(exename):
                self.logger.info('Start {0}'.format(exename))
            else:
                self.logger.error('Cannot start {0}'.format(exename))
