# MySQL
DATABASE = 'aijiu'
USERNAME = 'root'
PASSWORD = 'syt20010907'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 密钥（目前用不到）
SECRET_KEY = "absdjahjkwhkasdby1g26r6fsysvd"

# Neo4j
NEO4j_NAME = 'neo4j'
NEO4j_PASS = 'syt20010907'
NEO4j_GRAPH = 'neo4j'
