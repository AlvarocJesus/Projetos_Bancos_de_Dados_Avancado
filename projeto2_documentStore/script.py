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

# 4. Listar a média de salários de todos os professores em um determinado departamento  
def questao4(dept_name):
    try:
        print("Questão 4: Listar a média de salários de todos os professores em um determinado departamento\n")

        # remove os dados de alunos e professores do mongoDB
        deleteDataMongoDB('student')
        deleteDataMongoDB('instructor')
    
    # busca os dados de alunos no SQ
        instructorSQL = getDataSQLDB('select * from instructor;')
    
        instructorMongo = []
        for professor in instructorSQL:
            
            instructorMongo.append({
                "id": professor[0],
                "name": professor[1],
                "dept_name": professor[2],
                "salary": professor[3]
            })

        db.instructor.insert_many(instructorMongo)
    
        # Busca dados dos professores
        departmentSQL = getDataSQLDB('select * from department')
    
        departmentMongo = []

        for dept in departmentSQL:
            
            professoresID = [professoresID["_id"] for professoresID in instructorMongo if professoresID["dept_name"] == dept[0]]
            
            departmentMongo.append({
                "name": dept[0],
                "building": dept[1],
                "budget": dept[2],
            "professores": professoresID
            })
        db.department.insert_many(departmentMongo)
    
        # Busca no mongo - Resolver a questao
        department = db.department.find({ "name": dept_name })
	
        salarios = []
        for dept in department:
            salarios = [prof["salary"] for prof in instructorMongo if prof["dept_name"] == dept["name"]]
            
        media = sum(salarios) / len(salarios)
        print(f'Media: {media}')

    except Exception as e:
        print(f'Erro: {e}')

# 5. Recuperar o número total de créditos obtidos por um estudante específico 
def questao5(name):
    try:
        print("Questão 5: Recuperar o número total de créditos obtidos por um estudante específico\n")

        # remove os dados de alunos e professores do mongoDB
        deleteDataMongoDB('student')
    
        # busca os dados de alunos e professores no SQL
        alunosSQL = getDataSQLDB('select * from student;')
    
        alunorMongo = []
        for Aluno in alunosSQL:
            alunorMongo.append({
                "id": Aluno[0],
                "name": Aluno[1],
                "dept_name": Aluno[2],
                "tot_cred": Aluno[3]
            })
            
        db.student.insert_many(alunorMongo)    
        
        # Busca no mongo - Resolver a questao
        student = db.student.find({ "name": name })

        
        for aluno in student:
            if aluno["name"] == name:
                print(f'O aluno {aluno["name"]} tem {aluno["tot_cred"]} créditos')

    except Exception as e:
        print(f'Erro: {e}')
        
#6. Encontrar todas as disciplinas ministradas por um professor em um semestre específico
def questao6(professor_name, semester):
    try:
        print("Questão 6: Encontrar todas as disciplinas ministradas por um professor em um semestre específico\n")

        # remove os dados de professores e disciplinas do mongoDB
        deleteDataMongoDB('instructor')
        deleteDataMongoDB('teaches')

		# Busca dados das disciplinas ministradas
        teachesSQL = getDataSQLDB('select * from teaches')

        teachesMongo = []
        for teach in teachesSQL:
            teachesMongo.append({
                "course_id": teach[1],
                "id": teach[0],
                "sec_id": teach[2],
                "semester": teach[3],
                "year": teach[4]
            })
        
        db.teaches.insert_many(teachesMongo)


        # busca os dados de professores no SQL
        instructorSQL = getDataSQLDB('select * from instructor;')



        instructorMongo = []
        for professor in instructorSQL:
        
            professoresID = [professoresID["_id"] for professoresID in teachesMongo if professoresID["id"] == professor[0]]
            
            instructorMongo.append({
                "id": professor[0],
                "name": professor[1],
                "dept_name": professor[2],
                "salary": professor[3],
            "professores": professoresID
            })
        db.instructor.insert_many(instructorMongo)

        

        # Busca no mongo - Resolver a questao
        instructor = db.instructor.find({ "name": professor_name})
        for teach in instructor:
    
            for semestre in teach["professores"]:
                
                courses = db.teaches.find({"_id": semestre ,"semester": semester })
                for course in courses:
                    print(course)
                    print(f'O professor {teach["name"]} ministrou a disciplina {course["course_id"]} no semestre {course["semester"]}')

    except Exception as e:
        print(f'Erro: {e}')

# 7. Listar todos os estudantes que têm um determinado professor como orientador
def questao7():
	try:
		print("Questão 7")
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

		# Faz a macumba  - Resolver a questao
		professores = db.instructor.find({"name": "Srinivasan"})
  
		for prof in professores:
			for aluno in prof["students"]:
				alunos = db.student.find({"_id": aluno})
				for alu in alunos:
					print(f'O professor {prof["name"]} dá aula para {alu["name"]}')
		

	except Exception as e:
		print(f'Erro: {e}')

# 8. Recuperar todas as salas de aula sem um curso associado
def questao8():
	try:
		print("\nQuestão 8")
		# deleta os depts, salas e cursos
		deleteDataMongoDB('classroom')
		deleteDataMongoDB('course')
		deleteDataMongoDB('department')
		
		# busca no sql e insere no mongodb os cursos
		cursos = getDataSQLDB('select * from course;')
		cursoMongol = []
		for curso in cursos:
			cursoMongol.append({
				'course_id': curso[0],
				'tittle': curso[1],
				'dept_name': curso[2],
				'credits': curso[3]
			})
		
		db.couse.insert_many(cursoMongol)

		# busca no sql e insere no mongodb os cursos
		section = getDataSQLDB('select * from section;')

		secMongol = []
		for sec in section:
			sec_ID = [sec_ID["_id"] for sec_ID in cursoMongol if sec_ID["dept_name"] == curso[2]]

			secMongol.append({
				'course_id': sec[0],
				'sec_id': sec[1],
				'semester': sec[2],
				'year': sec[3],
				'building': sec[4],
				'room_number': sec[5],
				'time_slot_id': sec[6],
				'deptID': sec_ID
			})
		db.section.insert_many(secMongol)

		clsr = getDataSQLDB('select * from classroom')

		clrsMongol = []
		for cls in clsr:
			clsr_ID = [clsr_ID["_id"] for clsr_ID in secMongol if clsr_ID["deptID"] == sec_ID]
			

			clrsMongol.append({
				'building': cls[0],
				'room_number': cls[1],
				'capacity': cls[2],
				'sectionIds': clsr_ID
			})
		db.course.insert_many(clrsMongol)
		# Busca as salas sem cursos
		sectionEnd = db.section.find({"course_id": ""})
		for cl in sectionEnd:
				print(f'As salas sem cursos associados são: {cl["building"]}')
			
	except Exception as e:
		print(f'Erro: {e}')

#9. Encontrar todos os pré-requisitos de um curso específico
def questao9(cursoEspecifico):
	try:
		print("\nQuestão 9")
		# deleta os prereq e cursos
		deleteDataMongoDB('prereq')
		deleteDataMongoDB('course')

		# busca no sql e insere no mongodb os prereq
		prerequisitos = getDataSQLDB('select * from prereq;')
		preqMongo = []
		for preq in prerequisitos:
			preqMongo.append({
				'course_id': preq[0],
				'prereq_id': preq[1],
				})
		db.prereq.insert_many(preqMongo)

		# busca no sql e insere no mongodb os cursos
		cursos = getDataSQLDB('select * from course;')

		cursosMongo = []
		for curso in cursos:
			preqID = [preqID["_id"] for preqID in preqMongo if preqID["course_id"] == curso[0]]

			cursosMongo.append({
				'course_id': curso[0],
				'title': curso[1],
				'dept_name': curso[2],
				'credits': curso[3],
				'prerequisitos': preqID
			})
		
		db.course.insert_many(cursosMongo)

		# busca no mongodb os cursos e prereq
		cursosFinalMonngo = db.course.find({ "title": cursoEspecifico })
		for cursoFinalMongo in cursosFinalMonngo:
			for preqID in cursoFinalMongo['prerequisitos']:
				prerequisitos = db.prereq.find({ "_id": ObjectId(preqID) })
				for preq in prerequisitos:
					print(f'Para cursar {cursoFinalMongo["title"]} é necessário ter {preq["prereq_id"]}')

	except Exception as e:
		print(f'Erro: {e}')

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

questao1()
# questao2("BIO-101", "Summer")
# questao3("Intro. to Computer Science")
# questao4("Biology")
# questao5("Smith")
# questao6("Srinivasan", "Fall")
# questao7()
# questao8()
# questao9("Data Structures")
# questao10()
