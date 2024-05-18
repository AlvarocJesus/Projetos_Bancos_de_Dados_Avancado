import os
from neo4j import GraphDatabase
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

driver = GraphDatabase.driver(
  "neo4j+s://a38c18e1.databases.neo4j.io",
  auth = ("neo4j", "89cyD-kbrtzfBaJzrxTTy3hALKSDXxT2zxvHkyquzuQ")
)

connection = driver.verify_connectivity()
print(f'Conectado ao Neo4j: {connection}')

session = driver.session()
print(f'Sessão criada: {session}')

# Realiza o select no banco de dados SQL
def getDataSQLDB(query):
	try:
		# Cria uma conexão com o banco de dados
		engine = create_engine("postgresql://wpwvldie:FZJVGeEX5HWudTq769cmen4Ytxr-ixxL@silly.db.elephantsql.com/wpwvldie", echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		
		# Cria um cursor para executar as queries
		conn = engine.connect()
		
		# Executa a query
		data = conn.execute(text(query)).all()
		
		# Fecha a conexão
		session.close()
		
		return data
	except Exception as e:
		print(f"Deu errado {e}")

def deleteDataMongoDB(collection):
	try:
		db[collection].delete_many({})
	except Exception as e:
		print(f"Deu errado {e}")


# 1. Listar todos os cursos oferecidos por um determinado departamento
def questao1():
  
	teste = getDataSQLDB("select * from advisor;")
	print(teste)
  
  # Cria a query
	for adv in range(len(teste)):
		query = """
			match (i:instructor { id: '"""+adv[1]+"""' }),(s:student { id: '"""+adv[0]+"""' })
			create
			(i)-[:ADVISOR]->(s)
		"""
		result = session.run(query)
		print(f'Result: {result}')
  
#   # Executa a query
#   result = session.run(query)
  
#   # Imprime o resultado
#   for record in result:
#     print(record['c.name'])

# 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre

# 3. Encontrar todos os estudantes que estão matriculados em um curso específico

# 10. Recuperar a quantidade de alunos orientados por cada professor

questao1()