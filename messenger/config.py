BACKLOG = 10
SERVER_HOST = 'localhost'
SERVER_PORT = 5050

DB_ENGINE = 'postgresql+psycopg2://'
DB_USER = 'postgres'
DB_PASSWORD = '9w6sMnj1'
DB_HOST ='localhost'
DB_NAME = 'messenger'

DB_FULL_ENGINE = DB_ENGINE + DB_USER + ':' +DB_PASSWORD + '@' + DB_HOST + '/' + DB_NAME
