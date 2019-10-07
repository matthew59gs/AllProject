#!/usr/bin/env python

import log_monitor
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        log = dunhe_public.SetLog('log_monitor')
        date = sys.argv[1]
        oplus_log_path = sys.argv[2]
        pb_log_path = sys.argv[3]
        if len(sys.argv) >= 5:
            save_path = sys.argv[4]
        else:
            save_path = ""
        log.debug('date = {0}, oplus_log_path = {1}, pb_log_path = {2}, save_path={3}'.format(
            date, oplus_log_path, pb_log_path, save_path))

        oplus_log = log_monitor.OplusLogMonitor(log)
        oplus_log.set_date(date)
        oplus_log.set_log_path(oplus_log_path)
        oplus_log.set_result_path(save_path)
        oplus_log.find_result()

        pb_log = log_monitor.PBLogMonitor(log)
        pb_log.set_date(date)
        pb_log.set_log_path(pb_log_path)
        pb_log.set_result_path(save_path)
        pb_log.find_result()