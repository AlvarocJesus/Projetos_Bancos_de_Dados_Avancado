from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://alvimcoelhojesus:Wz5wyAvFghP6DCPs@projeto2documentstore.bv2jjzy.mongodb.net/?retryWrites=true&w=majority&appName=Projeto2DocumentStore"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.projeto2
# print(client.list_database_names())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!\n")
except Exception as e:
    print(e)

# 1. Listar todos os cursos oferecidos por um determinado departamento
# SQL
"""
select
  *
  -- d.*,
  -- c.id as courses
from department d
inner join course c on d.dept_name = c.dept_name
--order by d.dept_name
group by 1
"""
def questao1():
    try:
        departamento = db.department.find({}, { "_id": 0, "name": 1, "courses": 2 })
        for depart in departamento:
            for cursoId in depart['courses']:
                cursos = db.course.find({ "_id": ObjectId(cursoId) }, { "_id": 0, "course_id": 1, "title": 2  })
                for curso in cursos:
                    print(f'\nDepartamento: {depart["name"]}\tID do curso: {curso["course_id"]}\tNome do curso: {curso["title"]}')
    except Exception as e:
        print(f"Deu errado {e}")

# 2. Recuperar todas as disciplinas de um curso específico em um determinado semestre
def questao2():
    try:
        semestres = db
        for semestre in semestres:
            cursos = db
            for curso in cursos:
                disciplinas = db
                for disciplina in disciplinas:
                    print(f'Disciplina: {disciplina} do curso de {curso} no semestre {semestre}')
    except Exception as e:
        print(f'Deu ruim: {e}')

questao1()