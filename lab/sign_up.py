import random

def register(database, username, password, level):
    user_id = str(random.randint(1,100))
    database[user_id] = {'username': username,
                         'password': password,
                         'level': level}
    print(f'User {username} has already been record, User ID is {user_id}')
    return database, user_id