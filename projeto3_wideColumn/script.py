import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from time import sleep
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
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

- Questao 2
CREATE TABLE default_keyspace.section (
		course_id text,
		sec_id text,
		semester text,
		year text,
		building text,
		room_number text,
		time_slot_id text,
		PRIMARY KEY ((couse_id), sec_id, semester, year)
);
create index on default_keyspace.section(semester);

- Questao 3
CREATE TABLE default_keyspace.students_course (
		dept_name text,
		building text,
		budget text,
		course_id text,
		title text,
		credits text,
		id text,
		name text,
		tot_cred  text,
		PRIMARY KEY ((name), title, dept_name)
);
create index on default_keyspace.students_course(title);

- Questao 10
CREATE TABLE default_keyspace.students_teaches (
		id_instructor text,
		name text,
		salary text,
		id_student text,
		name_student text,
		dept_name text,
		tot_cred text,
		PRIMARY KEY ((name), name_student, dept_name)
);
"""

# Realiza o select no banco de dados SQL
def getDataSQLDB(query):
	try:
		print('Entrou na função getDataSQLDB')
		# Cria uma conexão com o banco de dados
		url = os.getenv('POSTGRESURLDB')
		print(url)
		engine = create_engine(url, echo=True)
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
def questao2(course, semester):
	try:
		print('Questao 2')
		
    # Deleta os dados da tabela
		deleteDataCassandraDB('section')
	
		sections = getDataSQLDB('select * from "section" s;')

		sectionsCassandra = []
		for section in sections:
			query = f"insert into default_keyspace.section(course_id, sec_id, semester, year, building, room_number, time_slot_id) values ('{section[0]}', '{section[1]}', '{section[2]}', '{section[3]}', '{section[4]}', '{section[5]}', '{section[6]}');"
			sectionsCassandra.append(session.execute(query))
			sleep(1)
		print('Adicionou os dados no Cassandra')

		sectionFinal = session.execute(f"select * from default_keyspace.section WHERE course_id = '{course}' AND semester = '{semester}';")
		for section in sectionFinal:
			print(f'Course ID: {section[0]}\tSection ID: {section[4]}\tSemester: {section[1]}\tYear: {section[6]}\tBuilding: {section[2]}\tRoom Number: {section[3]}\tTime Slot ID: {section[5]}')
	except Exception as e:
		print(f"Deu errado {e}")

# 3. Encontrar todos os estudantes que estão matriculados em um curso específico
def questao3(titleCourse):
	try:
		print('Questao 3')

		# Deleta os dados da tabela
		deleteDataCassandraDB('students_course')

		studentsCourse = getDataSQLDB("""
			select
				d.dept_name,
				d.building,
				d.budget,
				c.course_id,
				c.title,
				c.credits,
				s.id,
				s."name",
				s.tot_cred 
			from department d  
			inner join course c on d.dept_name = c.dept_name 
			inner join student s on c.dept_name = s.dept_name;""")

		studentsCourseCassandra = []
		for student in studentsCourse:
			query = f"insert into default_keyspace.students_course(dept_name, building, budget, course_id, title, credits, id, name, tot_cred) values ('{student[0]}', '{student[1]}', '{student[2]}', '{student[3]}', '{student[4]}', '{student[5]}', '{student[6]}', '{student[7]}', '{student[8]}');"
			studentsCourseCassandra.append(session.execute(query))
			sleep(1)
		print('Adicionou os dados no Cassandra')

		studentsCoursesCassandra = session.execute(f"select * from default_keyspace.students_course where title = '{titleCourse}'")
		for student in studentsCoursesCassandra:
			print(f'Curso: {student[1]}, tem o estudante {student[0]} matriculado')
	except Exception as e:
		print(f"Deu errado {e}")

#Questão 4: Listar a média de salários de todos os professores em um determinado departamento
def questao4(department_name):
	try:
		print('Questão 4: Listar a média de salários de todos os professores em um determinado departamento\n\n')
		# Obter dados do SQLDB
		professors_salaries = getDataSQLDB(f"""
		select name, dept_name, salary
		from instructor;
		""")

		# Inserir dados no CassandraDB
		for professor in professors_salaries:
			session.execute(f"""
			INSERT INTO default_keyspace.instructor_departament (dept_name, avg_salary, nome)
			VALUES ('{professor[1]}', '{professor[2]}','{professor[0]}');
			""")

		count = 0
		soma_salary = 0
		# Obter dados do CassandraDB
		professors = session.execute(f"SELECT avg_salary FROM default_keyspace.instructor_departament WHERE dept_name = '{department_name}';")
		for professor in professors:
			# calcular media de salarios
			soma_salary+= float(professor[0])
			count+=1
			
		print(f'A média de salários dos professores do departamento {department_name} é de R$ {soma_salary/count}\n')

	except Exception as e:
		print(f"Erro: {e}")
		
#Questão 5: Recuperar o número total de créditos obtidos por um estudante específico
def questao5(student_name):
	try:
		# Deleta dados antigos do CassandraDB para o estudante especificado
		deleteDataCassandraDB(f"DELETE FROM student WHERE name = '{student_name}'")

		# Obtém dados do SQLDB
		student_credits = getDataSQLDB(f"""
			SELECT name, tot_cred
			FROM student;""")

		print('Questão 5: Recuperar o número total de créditos obtidos por um estudante específico\n\n')

		# Verifica se student_credits não é None e insere no CassandraDB
	 

		for student in student_credits:
			# Insere dados no CassandraDB
			session.execute((f"""insert into default_keyspace.student (name, total_cred) VALUES ('{student[0]}', '{student[1]}');"""))

		student_credits_cassandra = session.execute(f"SELECT * FROM default_keyspace.student WHERE name = '{student_name}';")
		for student in student_credits_cassandra:
			print(f'O estudante {student[0]} possui um total de {student[1]} créditos\n')

	except Exception as e:
		print(f"Erro: {e}")
		
#Questão 6: Encontrar todas as disciplinas ministradas por um professor em um semestre específico
def questao6(professor_name, semester):
	try:
		print('Questão 6: Encontrar todas as disciplinas ministradas por um professor em um semestre específico\n\n')

		# Obter dados do SQLDB
		deleteDataCassandraDB('student')
		professor_courses = getDataSQLDB(f"""
			SELECT t.course_id, i.name, t.semester, i.id
			FROM teaches t
			JOIN instructor i ON i.ID = t.ID;""")

		# Inserir dados no CassandraDB
		for course in professor_courses:
			query = f"insert into default_keyspace.instructor_teaches(course_id, id, semester, name ) values ('{course[0]}','{course[3]}','{course[2]}','{course[1]}');"
			session.execute(query)
			sleep(1)
		print('Adicionou os dados no Cassandra')

		# Obter dados do CassandraDB
		professor_courses_cassandra = session.execute(f"select * from default_keyspace.instructor_teaches where name = '{professor_name}' and semester = '{semester}'")
		for course in professor_courses_cassandra:
			print(f'O professor {professor_name} ministra a disciplina {course[2]} no semestre {semester}\n')
 
	except Exception as e:
		print(f"Erro: {e}")

# 10. Recuperar a quantidade de alunos orientados por cada professor
def questao10():
	try:
		print('Questao 10')

		# Deleta os dados da tabela
		deleteDataCassandraDB('students_teaches')

		studentsTeaches = getDataSQLDB("""
			select 
				i.id as id_instructor
				, i."name"
				, i.salary 
				, s.id as id_student
				, s."name"
				, s.dept_name
				, s.tot_cred
			from instructor i
			inner join student s on i.dept_name = s.dept_name;""")

		for student in studentsTeaches:
			# print(f'Student: {student}')
			query = f"insert into default_keyspace.students_teaches(id_instructor, name, salary, id_student, name_student, dept_name, tot_cred) values ('{student[0]}', '{student[1]}', '{student[2]}', '{student[3]}', '{student[4]}', '{student[5]}', '{student[6]}');"
			session.execute(query)
			sleep(1)
		print('Adicionou os dados no Cassandra')

		studentsTeachesCassandra = session.execute('SELECT name, count(id_instructor)  FROM default_keyspace.students_teaches GROUP BY name;')
		
		for students in studentsTeachesCassandra:
			print(f'Professor {students[0]} orienta o aluno {students[1]}')
	except Exception as e:
		print(f"Deu errado {e}")

# questao1()
# questao2("BIO-101", "Summer")
# questao3("Intro. to Computer Science")
#questao4("Finance")
#questao5("Zhang")
#questao6("Srinivasan", "Fall")
questao10()
