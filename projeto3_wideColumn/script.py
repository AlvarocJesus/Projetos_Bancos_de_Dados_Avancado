import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from configparser import ConfigParser
from time import sleep
from dotenv import load_dotenv

load_dotenv()

session = Cluster(
    cloud={
			"secure_connect_bundle": os.getenv('SECURECONNECTBUNDLEPATH'),
			'connect_timeout': 30
		},
    auth_provider=PlainTextAuthProvider("token", os.getenv('astraToken')),
).connect()

print(f'Session: {session}')

# Cria todas as tabelas no banco Cassandra
"""
- Questao 1:
CREATE TABLE default_keyspace.course_department (
    dept_name text,
    building text,
    budget text,
    course_id text,
		title text,
		credits text,
    PRIMARY KEY (dept_name, course_id, title)
);
"""

# Realiza o select no banco de dados SQL
def getDataSQLDB(query):
	try:
		# Cria uma conexão com o banco de dados
		engine = create_engine(os.getenv('POSTGRESURLDB'), echo=True)
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

def deleteDataCassandraDB(collection):
	try:
		session.execute(f'truncate defaul_keyspace.{collection}')
	except Exception as e:
		print(f"Deu errado {e}")

# 1. Listar todos os cursos oferecidos por um determinado departamento
def questao1():
  try:
    print("Questão 1")
		
    # Deleta os dados da tabela
    deleteDataCassandraDB('course_department')
		
    cursos = getDataSQLDB("""
      select 
        *
      from department d 
      inner join course c on d.dept_name = c.dept_name;
    """)

    cursosCassandra = []
		
    for curso in cursos:
      query = f"INSERT INTO default_keyspace.course_department(dept_name, building, budget, course_id, title, credits) VALUES ('{curso[0]}', '{curso[1]}', '{curso[2]}', '{curso[3]}', '{curso[4]}', '{curso[6]}');"
      addCurso = session.execute(query)
      cursosCassandra.append(addCurso)
      sleep(1)
      		
    # Resolucao
    departamentosCursos = session.execute('select * from default_keyspace.course_department;')
    print('----------Cursos CASSANDRA----------')
    for curso in departamentosCursos:
      print(curso)

  except Exception as e:
    print(f"Deu errado {e}")

# 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre
def questao2():
	try:
		print('Questao 2')
		
    # Deleta os dados da tabela
		deleteDataCassandraDB('course_department')
	except Exception as e:
		print(f"Deu errado {e}")

questao1()
questao2()
# questao3()
# questao10()