# 查询用户
def find_id(database, user_id):
    if user_id in database:
        print(f'{user_id}: {database[user_id]['username']}')

## TODO 写一个函数，完成通过用户名查找用户是否存在的代码
def find_name(database, username):
    pass

    
# 用户登录
## TODO 完成对登录异常情况：用户名不存在 | 用户存在但密码错误的处理，统一print登录失败就可以
def login(database, username, password):
    for user_id in database:
        if database[user_id]['username'] == username:
            if database[user_id]['password'] == password:
                print(f'登录成功！用户级别为{database[user_id]['level']}')