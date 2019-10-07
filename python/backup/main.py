#coding = UTF-8
import sys
import backup_pb_log_dbf
sys.path.append("..\\..\\public\\python")
import dunhe_public


if __name__ == "__main__":
    '''
    sys.argv[1] HSPB or XTPB
    sys.argv[2] date, if null, then today
    sys.argv[3] log path
    sys.argv[4] hspb local str
    sys.argv[5] dbf path, not necessary
    '''
    if len(sys.argv) >= 4:
        log = dunhe_public.SetLog('backup-pb-log-dbf')
        pb_type = sys.argv[1]
        date = sys.argv[2]
        if date == "0":
            date = ""
        log_path = sys.argv[3]
        if pb_type.find("HSPB") >= 0:
            if len(sys.argv) >= 5:
                local_str = sys.argv[4]
                log.debug("pb_type = {0}, date = {1}, log_path={2}, local_str={3}".format(
                    pb_type, date, log_path, local_str))
                pb = backup_pb_log_dbf.HS_pb_backup(log=log, local_str=local_str, date=str(date))
                pb.backup_log(log_path)
                if len(sys.argv) >= 6:
                    pb.backup_dbf(sys.argv[5])
        elif pb_type.find("XTPB") >= 0:
            log.debug("pb_type = {0}, date = {1}, log_path={2}".format(pb_type, date, log_path))
            pb = backup_pb_log_dbf.XT_pb_backup(log, date=date)
            pb.backup_log(log_path)
