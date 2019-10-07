import sys
sys.path.append("..\\..\\..\\public\\python")
import dunhe_public
import pymysql
import re

logger = dunhe_public.SetLog('TEST')
target_str = ['OUTER_tstockinfo_future', 'tfuturekind', 'tdepositset_future']
for target in target_str:
    re_str = 't(?!his)\w*'
    match = re.match(re_str, target)
    if match:
        print(match)

# try:
#     connection = pymysql.connect(host='192.168.40.202', port=3306,
#                              user='oplus', password='oplus',
#                              db='oplus_p', charset='utf8')
# except Exception as e:
#     logger.error("Sever connect fail: {0}".format(e))
# else:
#     try:
#         cursor = connection.cursor()
#         sql = 'show tables;'
#         cursor.execute(sql)
#         data = cursor.fetchall()
#         print(data)
#     finally:
#         cursor.close()
#         connection.close()
