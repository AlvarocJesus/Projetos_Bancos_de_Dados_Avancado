import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

driver = GraphDatabase.driver(
  os.getenv("NEO4J_URI"),
  auth = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

connection = driver.verify_connectivity()
print(f'Conectado ao Neo4j: {connection}')

session = driver.session()
print(f'Sessão criada: {session}')

# Realiza o select no banco de dados SQL
def getDataSQLDB(query):
	try:
		# Cria uma conexão com o banco de dados
		engine = create_engine(os.getenv('POSTGRESURLDB'), echo=False)
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
	# Cria a query
  query = """
    MATCH (d:Department {name: 'Computer Science'})-[:HAS_COURSE]->(c:Course)
    RETURN c.name
  """
  
  # Executa a query
  result = session.run(query)
  
  # Imprime o resultado
  for record in result:
    print(record['c.name'])

# 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre

# 3. Encontrar todos os estudantes que estão matriculados em um curso específico

# 10. Recuperar a quantidade de alunos orientados por cada professor

questao1()