import os
import getpass
import platform

user_name = getpass.getuser()

# windows 系统下载文件放在哪个目录下
# 目前根据锁屏时名字 在C 盘下面的 Users/锁屏名字/Desktop/kmlfile 下面
if platform.system().lower() == 'windows':
    FILEPATH = "C:\\Users\\{}\\Desktop\\kmlfile\\".format(user_name)
    UPLOAD_PATH = "C:\\Users\\{}\\Desktop".format(user_name)
else:
    FILEPATH = "/Users/{}/Desktop/kmlfile/".format(user_name)
    UPLOAD_PATH = "/Users/{}/Desktop".format(user_name)

EXPIRED_DATE = '3000-09-30 00:00:00'

EXPIRED_WARN = "错误反馈QQ:1550847027"

if not os.path.exists(FILEPATH):
    os.mkdir(FILEPATH)



