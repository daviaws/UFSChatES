import sqlite3

CREATE_USERS =     '''
            CREATE TABLE users
            (
            name         TEXT    PRIMARY KEY,
            password     TEXT
            );
            '''

INSERT_USER =   '''INSERT INTO users VALUES (?, ?);'''

SELECT_ALL_USERS = '''SELECT * FROM users;'''

class Database():

    def __init__(self, db_file):
        self.db_file = db_file
        self.db_connection = sqlite3.connect(self.db_file)
        self.db_cursor = self.db_connection.cursor()
    
    def create_tables(self):
        self.db_cursor.execute(CREATE_USERS)
        self.db_connection.commit()
        
    def insert_user(self, user):
        self.db_cursor.execute(INSERT_USER,(user['user'], user['password']))
        self.db_connection.commit()
    
    def select_all_users(self):
        self.db_cursor.execute(SELECT_ALL_USERS)
        res = self.db_cursor.fetchall()
        return res