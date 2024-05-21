import os
from neo4j import GraphDatabase
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from time import sleep

""" driver = GraphDatabase.driver(
  "neo4j+s://a38c18e1.databases.neo4j.io",
  auth = ("neo4j", "89cyD-kbrtzfBaJzrxTTy3hALKSDXxT2zxvHkyquzuQ")
)

session = driver.session()
print(f'Sessão criada: {session}') """

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
def questao1(driver, dept_name):
  
	teste = getDataSQLDB("select * from course;")
  
  # Cria a query
	query = "MATCH (d:department { dept_name: '" + dept_name + "' }) WITH d MATCH (c:course) RETURN d, c;"
	# result = session.run(query)
	result, summary, keys = driver.execute_query(query)

	# Exibe o resultado
	for item in result:
		# print(item.data())
		print(f"Departamento: {item['d']['dept_name']} tem o curso {item['c']['course_id']} - {item['c']['title']}")
			
# 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre
def questao2(driver):
  
	teste = getDataSQLDB("select * from course;")
  
  # Cria a query
	query = 'MATCH p=(course { title: "Computational Biology" })-[:section {semester: "Summer"}]->() RETURN p;'
	# result = session.run(query)
	result, summary, keys = driver.execute_query(query)

	# Exibe o resultado
	for item in result:
		print(item.data())
		# print(f"course_id: {item['p']['course_id']}, credits: {item['p']['credits']}, dept_name: {item['p']['dept_name']}, title: {item['p']['title']}, room_number: {item['section']['room_number']}, building: {item['section']['building']}, capacity: {item['section']['capacity']}")

# 3. Encontrar todos os estudantes que estão matriculados em um curso específico
def questao3(driver):
  
	teste = getDataSQLDB("select * from course;")
  
  # Cria a query
	query = "MATCH (c:course) with c MATCH (s:student) return s, c;"
	# result = session.run(query)
	result, summary, keys = driver.execute_query(query)

	# Exibe o resultado
	for item in result:
		# print(item.data())
		print(f"O aluno {item['s']['name']} está matriculado no curso {item['c']['course_id']} - {item['c']['title']}")

# Questão 4: Listar a média de salários de todos os professores em um determinado departamento
def questao4(department_name, driver):
	# Cria a query
	query = f"MATCH (s:instructor) WHERE s.dept_name = '{department_name}' RETURN s.salary;"

	# Executa a query
	result, summary, keys = driver.execute_query(query)

	cout = 0 
	soma = 0
	for record in result:
		cout += 1
		soma += int(record['s.salary'])

	print(f"A média de salários dos professores do departamento {department_name} é de R${soma/cout:.2f}\n")

#Questão 5: Recuperar o número total de créditos obtidos por um estudante específico pelo nome
def questao5(student_name, driver):
	# Cria a query
	query = f"MATCH (s:student) WHERE s.name = '{student_name}' RETURN s;"

	# Executa a query
	result, summary, keys = driver.execute_query(query)


	# Imprime o resultado
	for record in result:
		print(record.data())
		print(f"O estudante {record['s']['name']} possui um total de {record['s']['tot_cred']} créditos\n")

#Questão 6: Encontrar todas as disciplinas ministradas por um professor em um semestre específico
def questao6(instructor_name, semester, driver):
	# Cria a query
	query = "MATCH p=({name: '"+instructor_name+"'})-[:teaches{semester: '"+semester+"'}]->() RETURN p;"

	# Executa a query
	result, summary, keys = driver.execute_query(query)


	# Imprime o resultado
	for record in result:
		print(record.data())
		# print(f"O professor {instructor_name} ministrou as seguintes disciplinas no semestre {semester}:")

# 10. Recuperar a quantidade de alunos orientados por cada professor
def questao10(driver, instructor):
  
	teste = getDataSQLDB("select * from course;")
  
  # Cria a query
	query = "MATCH p=({ name: '" + instructor + "' })-[:ADVISOR]->() RETURN p;"
	# result = session.run(query)
	result, summary, keys = driver.execute_query(query)

	# Exibe o resultado
	for item in result:
		print(item.data())
		# print(f"Departamento: {item['d']['dept_name']} tem o curso {item['c']['course_id']} - {item['c']['title']}")

def teste(driver):
	teste = getDataSQLDB("select * from takes;")

	for t in teste:
		query = "match (s:student { id: '" + str(t[0]) + "' }), (sec:section { course_id: '" +t[1]+"', sec_id: "+str(t[2])+", semester: '"+t[3]+"', year: "+str(t[4])+" }) create (s)-[:TAKES { grade: '"+str(t[5])+"' }]->(sec)"
		result, k, c = driver.execute_query(query)
		sleep(1)
	
	result, k, c = driver.execute_query("match p=()-[:TAKES]->() return p;")
	for res in result:
		print(res.data())

with GraphDatabase.driver("neo4j+s://a38c18e1.databases.neo4j.io", auth=("neo4j","89cyD-kbrtzfBaJzrxTTy3hALKSDXxT2zxvHkyquzuQ")) as driver:
		driver.verify_connectivity()
		teste(driver)
		# questao1(driver, 'Comp. Sci.')
		# questao2(driver)
		# questao3(driver)
		#questao4("Finance", driver)
		#questao5("Zhang", driver)
		questao6("Zhang", "Fall", driver)
		# questao10(driver, 'Einstein')
