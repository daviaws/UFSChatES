import os
import json
import database

class Configation():
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.configarations = {}
        
        self.db = None
        
        self.load_config()

    def load_file(self):
        file = open(self.config_file, 'r')
        read = "".join(file.readlines())
        read = read.replace('\n', '')
        read = json.loads(read)
        self.configarations = read
    
    def init_db(self):
        db_path = self.configarations['db_path']
        db_file = db_path + '/' + self.configarations['db_file']
        
        if not os.path.isdir(db_path):
            os.makedirs(db_path)
            
        if not os.path.isfile(db_file):
            self.db = database.Database(db_file)
            self.db.create_tables()
        else:
            self.db = database.Database(db_file)
            
    def load_config(self):
        self.load_file()
        self.init_db()
        
        
        
Configation('config.chat')
