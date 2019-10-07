import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import log_monitor


def oplus_log_test(log=None, date='', oplus_log_path='', save_path=''):
    oplus_log = log_monitor.OplusLogMonitor(log)
    oplus_log.set_date(date)
    oplus_log.set_log_path(oplus_log_path)
    oplus_log.set_result_path(save_path)
    oplus_log.find_result()


def pb_log_test(log=None, date='', pb_log_path='', save_path=''):
    pb_log = log_monitor.PBLogMonitor(log)
    pb_log.set_date(date)
    pb_log.set_log_path(pb_log_path)
    pb_log.set_result_path(save_path)
    pb_log.find_result()


# date = '20190822'
date = '0'
log_path = 'G:\\data\\log'
log = dunhe_public.SetLog('log_monitor')

oplus_log_test(log=log, date=date, oplus_log_path=log_path, save_path=log_path)
pb_log_test(log=log, date=date, pb_log_path=log_path, save_path=log_path)

