import time
import random

from sqlalchemy import create_engine

db_name = 'database'
db_user = 'docker'
db_pass = 'docker'
db_host = 'database'
db_port = '5432'


db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

'''
def add_new_row(username, command):

    db.execute("INSERT INTO statistics (id,username,command) "+\
        "VALUES ("+ \ 
        str(username) + "," + \
        str(command) + ");" ) 
'''


