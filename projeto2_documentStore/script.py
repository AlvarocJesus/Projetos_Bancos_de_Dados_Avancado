import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODBURI'), server_api=ServerApi('1'))
db = client.projeto2

# Send a ping to confirm a successful connection
try:
	client.admin.command('ping')
	print("Pinged your deployment. You successfully connected to MongoDB!\n")
except Exception as e:
	print(e)

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
	try:
		print("Questão 1")

		# Deleta todos os cursos e departamentos do mongodb
		deleteDataMongoDB('course')
		deleteDataMongoDB('department')
		
		# busca no sql e insere no mongodb os cursos - OK
		cursosMongo = []
		cursos = getDataSQLDB('select * from course;')

		for curso in cursos:
			cursosMongo.append({
				"course_id": curso[0],
				"title": curso[1],
				"dept_name": curso[2],
				"credits": curso[3]
			})

		db.course.insert_many(cursosMongo)
		
		# busca no sql e insere no mongodb os departamentos
		departamentos = getDataSQLDB('select * from department;')

		departamentosFormatado = []
		for departamento in departamentos:
			cursosID = [cursoMongo['_id'] for cursoMongo in cursosMongo if cursoMongo['dept_name'] == departamento[0]]

			departamentosFormatado.append({
				"dept_name": departamento[0],
				"building": departamento[1],
				"budget": departamento[2],
				"courses": cursosID
			})
		
		db.department.insert_many(departamentosFormatado)

		# busca no mongodb os departamentos e cursos
		departamento = db.department.find({})
		
		for depart in departamento:
			for cursoId in depart['courses']:
				cursos = db.course.find({ "_id": ObjectId(cursoId) })
				for curso in cursos:
					print(f'Departamento: {depart["dept_name"]}\tID do curso: {curso["course_id"]}\tNome do curso: {curso["title"]}')
	except Exception as e:
		print(f"Deu errado {e}")

# 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre
def questao2(course, semester):
	try:
		print("\nQuestão 2")

		deleteDataMongoDB('section')

		section = getDataSQLDB('select * from section;')

		sectionMongo = []

		for sec in section:
			sectionMongo.append({
				"course_id": sec[0],
				"sec_id": sec[1],
				"semester": sec[2],
				"year": sec[3],
				"building": sec[4],
				"room_number": sec[5],
				"time_slot_id": sec[6]
			})
		
		db.section.insert_many(sectionMongo)

		sectionsMongo = db.section.find({
			'$or': [
				{ "course_id": course },
				{ "semester": semester }
			]
		})
		
		for section in sectionsMongo:
			print(f'Course ID: {section["course_id"]}\tSection ID: {section["sec_id"]}\tSemester: {section["semester"]}\tYear: {section["year"]}\tBuilding: {section["building"]}\tRoom Number: {section["room_number"]}\tTime Slot ID: {section["time_slot_id"]}')
	except Exception as e:
		print(f'Deu ruim: {e}')

# 3. Encontrar todos os estudantes que estão matriculados em um curso específico
def questao3(nomeCurso):
	try:
		print("\nQuestão 3")
		# deleta os alunos e cursos
		deleteDataMongoDB('student')
		deleteDataMongoDB('course')

		# busca no sql e insere no mongodb os alunos
		alunos = getDataSQLDB('select * from student;')

		alunosMongo = []
		for aluno in alunos:
			alunosMongo.append({
				'id': aluno[0],
				'name': aluno[1],
				'dept_name': aluno[2],
				'tot_cred': aluno[3]
			})
		
		db.student.insert_many(alunosMongo)

		# busca no sql e insere no mongodb os cursos
		cursos = getDataSQLDB('select * from course;')

		cursosMongo = []
		for curso in cursos:
			alunosID = [alunoID["_id"] for alunoID in alunosMongo if alunoID["dept_name"] == curso[2]]

			cursosMongo.append({
				'course_id': curso[0],
				'title': curso[1],
				'dept_name': curso[2],
				'credits': curso[3],
				"students": alunosID
			})
		
		db.course.insert_many(cursosMongo)

		# busca no mongodb os cursos e alunos
		cursosFinalMonngo = db.course.find({ "title": nomeCurso })
		for cursoFinalMongo in cursosFinalMonngo:
			for alunoID in cursoFinalMongo['students']:
				alunos = db.student.find({ "_id": ObjectId(alunoID) })
				for aluno in alunos:
					print(f'No curso de {cursoFinalMongo["title"]} estao matriculados os alunos {aluno["name"]}')
	except Exception as e:
		print(f'Deu ruim: {e}')

# 10. Recuperar a quantidade de alunos orientados por cada professor
def questao10():
	try:
		print("\nQuestão 10")
		# remove os dados de alunos e professores do mongoDB
		deleteDataMongoDB('student')
		deleteDataMongoDB('instructor')
    
    # busca os dados de alunos no SQL
		alunosSQL = getDataSQLDB('select * from student;')
    
		alunosMongo = []
    
		for aluno in alunosSQL:
			alunosMongo.append({
				"id": aluno[0],
				"name": aluno[1],
				"dept_name": aluno[2],
				"tot_cred": aluno[3]
			})
    
		db.student.insert_many(alunosMongo)
    
		# Busca dados dos professores
		professoresSQL = getDataSQLDB('select * from instructor')
    
		professoresMongo = []
    
		for prof in professoresSQL:
			alunosID = [alunoID["_id"] for alunoID in alunosMongo if alunoID["dept_name"] == prof[2]]
     
			professoresMongo.append({
				"id": prof[0],
				"name": prof[1],
				"dept_name": prof[2],
				"salary": prof[3],
    		"students": alunosID
			})
		
		db.instructor.insert_many(professoresMongo)
    
		# Busca no mongo - Resolver a questao
		professores = db.instructor.find({})
  
		for prof in professores:
			print(f'O professor {prof["name"]} do departamento de {prof["dept_name"]}, tem {len(prof["students"])} estudantes')
	except Exception as e:
		print(f'Erro: {e}')

# questao1()
# questao2("BIO-101", "Summer")
# questao3("Intro. to Computer Science")
questao10()