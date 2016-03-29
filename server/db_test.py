import os
import database

db_name = 'test1'

create_routine = True

if os.path.isfile(db_name):
    create_routine = False

db = database.Database(db_name)

if create_routine:
    db.create_tables()
    
    user1 = {'user' : 'gomman', 'password' : '1234'}
    user2 = {'user' : 'b', 'password' : 'shurupinga'}
    
    db.insert_user(user1)
    db.insert_user(user2)

print(db)   
res = db.select_all_users()
print(res)

#print(db.__dict__)
