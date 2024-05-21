import os
from neo4j import GraphDatabase
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# Realiza o select no banco de dados SQL
def getDataSQLDB(query):
	try:
		sleep(3)
		# Cria uma conexão com o banco de dados
		engine = create_engine(os.getenv("POSTGRESURLDB"), echo=False)
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

def deleteDataNeo4J(driver):
	try:
		driver.execute_query("""
			MATCH (i:instructor) DELETE i;
			MATCH (s:student) DELETE s;
			MATCH (c:classroom) DELETE c;
			MATCH p=()-[:PREREQ]->() DELETE p;
			MATCH (c:course) DELETE c;
			MATCH (d:department) DELETE d;
			MATCH (s:section) DELETE s;
		""")
	except Exception as e:
		print(f"Deu errado {e}")

def insertInstructor(driver):
	print("Inserindo Instructors")
	instructors = getDataSQLDB("select * from instructor;")

	for instructor in instructors:
		# id, name, dept_name, salary
		driver.execute_query("CREATE (:instructor { id: '" + instructor[0] + "', name: '" + instructor[1] + "', dept_name: '" + instructor[2] + "', salary: " + str(instructor[3]) + " });")
		sleep(1)
	sleep(3)

def insertStudents(driver):
	# Cria os Student
		print("Inserindo Students")
		students = getDataSQLDB("select * from student;")

		for student in students:
			driver.execute_query("CREATE (:student { id: '" + student[0] + "', name: '" + student[1] + "', dept_name: '" + student[2] + "', tot_cred: " + str(student[3]) + " });")
			sleep(1)
		sleep(3)

def insertCourses(driver):
	# Cria os Courses
		print("Inserindo Courses")
		courses = getDataSQLDB("select * from course c;")

		for course in courses:
			driver.execute_query("CREATE (:course { course_id: '" + course[0] + "', title: '" + course[1] + "', dept_name: '" + course[2] + "', credits: " + str(course[3]) + " });")
			sleep(1)
		sleep(3)

def insertClassroom(driver):
	# Cria os Classroom
		print("Inserindo Classrooms")
		classrooms = getDataSQLDB("select * from classroom;")

		for classroom in classrooms:
			driver.execute_query("CREATE (:classroom { building: '" + classroom[0] + "', room_number: " + str(classroom[1]) + ", capacity: " + str(classroom[2]) + " });")
			sleep(1)
		sleep(3)

def insertDepartment(driver):
	# Cria os Department
	print("Inserindo Departments")
	departments = getDataSQLDB("select * from department;")

	for department in departments:
		driver.execute_query("CREATE (:department { dept_name: '" + department[0] + "', building: '" + department[1] + "', budget: " + str(department[2]) + " });")
		sleep(1)
	sleep(3)

def insertTime_Slots(driver):
	# Cria os Time_slot
	print("Inserindo Time_slots")
	time_slots = getDataSQLDB("select * from time_slot;")

	for time_slot in time_slots:
		driver.execute_query("CREATE (:time_slot { time_slot_id: '" + time_slot[0] + "', day: '" + time_slot[1] + "', start_hr: " + time_slot[2] + ", start_min: " + time_slot[3] + ", end_hr: " + time_slot[4] + ", end_min: " + time_slot[5] + " });")
		sleep(1)
	sleep(3)

def insertSection(driver):
	# Cria os Section
		print("Inserindo Sections")
		sections = getDataSQLDB("select * from section;")
		for section in sections:
			driver.execute_query("CREATE (:section { course_id: '" + section[0] + "', sec_id: " + str(section[1]) + ", semester: '" + section[2] + "', year: " + str(section[3]) + ", building: '" + section[4] + "', room_number: " + section[5] + ", time_slot_id: '" + section[6] + "' });")
			sleep(1)
		sleep(3)

def insertPREREQ(driver):
	# PREREQ
	print("Inserindo Prereqs")
	prereqs = getDataSQLDB("select * from prereq;")
	for prereq in prereqs:
		driver.execute_query("MATCH (c1:course { course_id: '" + prereq[0] + "' }) MATCH (c2:course { course_id: '" + prereq[1] + "' }) CREATE (c1)-[:PREREQ]->(c2);")
		sleep(1)
	sleep(3)

def insertTEACHES(driver):
	# TEACHES
	print("Inserindo Teaches")
	teaches = getDataSQLDB("select * from teaches;")
	for teach in teaches:
		query = "MATCH (i:instructor { id: '" + str(teach[0]) + "' }), (s:section { sec_id: " + str(teach[2]) + ", course_id: '" + teach[1] + "', semester: '" + teach[3] + "', year: " + str(teach[4]) + " }) CREATE (i)-[:TEACHES]->(s);"
		driver.execute_query(query)
		sleep(1)
	sleep(3)

def insertADVISOR(driver):
	# ADVISOR
	print("Inserindo Advisors")
	advisors = getDataSQLDB("select * from advisor;")
	for advisor in advisors:
		driver.execute_query("MATCH (s:student { id: '" + advisor[0] + "' }) MATCH (i:instructor { id: '" + advisor[1] + "' }) CREATE (i)-[:ADVISOR]->(s);")
		sleep(1)
	sleep(3)

def insertTAKES(driver):
	# TAKES
	print("Inserindo Takes")
	takes = getDataSQLDB("select * from takes;")
	for take in takes:
		query = "MATCH (s:student { id: '" + str(take[0]) + "' }), (sec:section { sec_id: " + str(take[2]) + ", course_id: '" + take[1] + "', semester: '" + take[3] + "', year: " + str(take[4]) + " }) CREATE (s)-[:TAKES { grade: '" + take[5] + "' }]->(sec);"
		print(query)
		driver.execute_query(query)
		sleep(1)
	sleep(3)

def insertClassroom_Section(driver):
	# Classroom - Section
	print("Inserindo Classroom - Section")
	# classroom_sections = getDataSQLDB('select * from classroom natural join "section";')
	classroom_sections = getDataSQLDB('select * from "section";')
	for classroom_section in classroom_sections:
		# driver.execute_query("MATCH (c:classroom { building: '" + classroom_section[0] + "', room_number: " + classroom_section[1] + " }) MATCH (s:section { sec_id: '" + classroom_section[4] + "', course_id: '" + classroom_section[3] + "', semester: '" + classroom_section[5] + "', year: " + classroom_section[6] + " }) CREATE (c)-[:CLASSROOM_SECTION]->(s);")
		driver.execute_query("MATCH (c:classroom { building: '" + classroom_section[4] + "', room_number: " + str(classroom_section[5]) + " }) MATCH (s:section { sec_id: " + str(classroom_section[1]) + ", course_id: '" + classroom_section[0] + "', semester: '" + classroom_section[2] + "', year: " + str(classroom_section[3]) + " }) CREATE (c)-[:CLASSROOM_SECTION]->(s);")
		sleep(1)
	sleep(3)

def insertTime_slot_Section(driver):
	# Time_slot - Section
	print("Inserindo Time_slot - Section")
	# time_slot_sections = getDataSQLDB('select * from time_slot natural join "section";')
	time_slot_sections = getDataSQLDB('select * from "section";')
	for time_slot_section in time_slot_sections:
		# driver.execute_query("MATCH (t:time_slot { time_slot_id: '" + time_slot_section[0] + "', day: '" + time_slot_section[1] + "', start_hr: " + time_slot_section[2] + ", start_min: " + time_slot_section[3] + ", end_hr: " + time_slot_section[4] + ", end_min: " + time_slot_section[5] + " }) MATCH (s:section { sec_id: '" + time_slot_section[7] + "', course_id: '" + time_slot_section[6] + "', semester: '" + time_slot_section[8] + "', year: " + time_slot_section[9] + " }) CREATE (t)-[:TIME_SLOT_SECTION]->(s);")
		driver.execute_query("MATCH (t:time_slot { time_slot_id: '" + time_slot_section[6] + "' }) MATCH (s:section { sec_id: " + str(time_slot_section[1]) + ", course_id: '" + time_slot_section[0] + "', semester: '" + time_slot_section[2] + "', year: " + str(time_slot_section[3]) + " }) CREATE (t)-[:TIME_SLOT_SECTION]->(s);")
		sleep(1)
	sleep(3)

def insertSection_Course(driver):
	# Section - Course
	print("Inserindo Section - Course")
	# section_courses = getDataSQLDB('select * from "section" natural join course;')
	section_courses = getDataSQLDB('select * from "section";')
	for section_course in section_courses:
		# driver.execute_query("MATCH (s:section { sec_id: '" + section_course[1] + "', course_id: '" + section_course[0] + "', semester: '" + section_course[2] + "', year: " + section_course[3] + " }) MATCH (c:course { course_id: '" + section_course[0] + "', title: '" + section_course[7] + "', dept_name: '" + section_course[8] + "', credits: " + section_course[9] + " }) CREATE (s)-[:SECTION_COURSE]->(c);")
		driver.execute_query("MATCH (s:section { sec_id: " + str(section_course[1]) + ", course_id: '" + section_course[0] + "', semester: '" + section_course[2] + "', year: " + str(section_course[3]) + " }) MATCH (c:course { course_id: '" + section_course[0] + "' }) CREATE (s)-[:SECTION_COURSE]->(c);")
		sleep(1)
	sleep(3)

def insertInstructor_Department(driver):
	# Instructor - Department
	print("Inserindo Instructor - Department")
	# instructor_departments = getDataSQLDB('select * from instructor natural join department;')
	instructor_departments = getDataSQLDB('select * from instructor;')
	for instructor_department in instructor_departments:
		# driver.execute_query("MATCH (i:instructor { id: '" + instructor_department[0] + "' }) MATCH (d:department { dept_name: '" + instructor_department[2] + "', building: '" + instructor_department[4] + "', budget: " + instructor_department[5] + " }) CREATE (i)-[:INSTRUCTOR_DEPARTMENT]->(d);")
		driver.execute_query("MATCH (i:instructor { id: '" + instructor_department[0] + "' }) MATCH (d:department { dept_name: '" + instructor_department[2] + "' }) CREATE (i)-[:INSTRUCTOR_DEPARTMENT]->(d);")
		sleep(1)
	sleep(3)

def insertStudent_Department(driver):
	# Student - Department
	print("Inserindo Student - Department")
	# student_departments = getDataSQLDB('select * from student natural join department;')
	student_departments = getDataSQLDB('select * from student;')
	for student_department in student_departments:
		# driver.execute_query("MATCH (s:student { id: '" + student_department[0] + "' }) MATCH (d:department { dept_name: '" + student_department[2] + "', building: '" + student_department[4] + "', budget: " + student_department[5] + " }) CREATE (s)-[:STUDENT_DEPARTMENT]->(d);")
		driver.execute_query("MATCH (s:student { id: '" + student_department[0] + "' }) MATCH (d:department { dept_name: '" + student_department[2] + "' }) CREATE (s)-[:STUDENT_DEPARTMENT]->(d);")
		sleep(1)
	sleep(3)

def insertDepartment_Course(driver):
	# Department - Course
	print("Inserindo Department - Course")
	# department_courses = getDataSQLDB('select * from department natural join course;')
	department_courses = getDataSQLDB('select * from course;')
	for department_course in department_courses:
		# driver.execute_query("MATCH (d:department { dept_name: '" + department_course[2] + "', building: '" + department_course[4] + "', budget: " + department_course[5] + " }) MATCH (c:course { course_id: '" + department_course[0] + "', title: '" + department_course[1] + "', credits: " + department_course[3] + " }) CREATE (d)-[:DEPARTMENT_COURSE]->(c);")
		driver.execute_query("MATCH (d:department { dept_name: '" + department_course[2] + "' }) MATCH (c:course { course_id: '" + department_course[0] + "', title: '" + department_course[1] + "' }) CREATE (d)-[:DEPARTMENT_COURSE]->(c);")
		sleep(1)

def insertDataNeo4J(driver):
	try:
		print("Inserindo dados no Neo4J")
		insertInstructor(driver)
		sleep(2)
		insertStudents(driver)
		sleep(2)
		insertCourses(driver)
		sleep(2)
		insertClassroom(driver)
		sleep(2)
		insertDepartment(driver)
		sleep(2)
		insertTime_Slots(driver)
		sleep(2)
		insertSection(driver)
		sleep(2)
		
		# Cria os Relacionamentos
		insertPREREQ(driver)
		sleep(2)
		insertTEACHES(driver)
		sleep(2)
		insertADVISOR(driver)
		sleep(2)
		insertTAKES(driver)
		sleep(2)
		insertClassroom_Section(driver)
		sleep(2)
		insertTime_slot_Section(driver)
		sleep(2)
		insertSection_Course(driver)
		sleep(2)
		insertInstructor_Department(driver)
		sleep(2)
		insertStudent_Department(driver)
		sleep(2)
		insertDepartment_Course(driver)
		sleep(2)

		print("Dados inseridos no Neo4J")
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

with GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"),os.getenv("NEO4J_PASSWORD"))) as driver:
		driver.verify_connectivity()
		# deleteDataNeo4J(driver)
		# insertDataNeo4J(driver)
		
		questao1(driver, 'Comp. Sci.')
		# teste(driver)
		# questao1(driver, 'Comp. Sci.')
		# questao2(driver)
		# questao3(driver)
		#questao4("Finance", driver)
		#questao5("Zhang", driver)
		# questao6("Zhang", "Fall", driver)
		# questao10(driver, 'Einstein')
