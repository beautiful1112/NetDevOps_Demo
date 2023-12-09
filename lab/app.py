import time
from sign_up import *
from sign_in import *


database = {}
username = input('请输入用户名：')
password = input('请输入密码：')

database, user_id = register(database, username, password, '3')
time.sleep(2)

find_id(database, user_id)
time.sleep(2)

login(database, username, password)
time.sleep(2)