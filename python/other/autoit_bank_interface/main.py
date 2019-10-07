# utf-8

import auto_bank_interface
import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public

if __name__ == '__main__':
    if len(sys.argv) > 1:
        log = dunhe_public.SetLog("auto_bank_interface")
        auto_run = auto_bank_interface.AutoRobot(log)
        auto_run.start_bank_interface(path=sys.argv[1], password=sys.argv[2])
