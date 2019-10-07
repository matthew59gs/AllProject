
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import auto

##bat的命令参数
##python auto_ risk_data_manage
if __name__ == '__main__':
    if len(sys.argv) > 1:
        logger = dunhe_public.SetLog("auto_start")
        auto_instance = auto.AutoStartExe(logger)
        auto_instance.load_config(sys.argv[1])
        auto_instance.run_config()
