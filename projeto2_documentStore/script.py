from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, insert, select, text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# username = 'professor'
# password = 'FgEp9W9qKAuaAodE'

username = 'alvimcoelhojesus'
password = 'Wz5wyAvFghP6DCPs'
uri = f"mongodb+srv://{username}:{password}@projeto2documentstore.bv2jjzy.mongodb.net/?retryWrites=true&w=majority&appName=Projeto2DocumentStore"

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


# Realiza o select no banco de dados SQL
def getDataSQLDB(query):
    try:
        # Cria uma conexão com o banco de dados
        engine = create_engine('postgresql://wpwvldie:FZJVGeEX5HWudTq769cmen4Ytxr-ixxL@silly.db.elephantsql.com/wpwvldie', echo=True)
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
    """
    db.course.delete_many({
        "course_id": { "$exists": True }
    })
    db.department.delete_many({
        "dept_name": { "$exists": True }
    })
    """
    try:
        db[collection].delete_many({})
    except Exception as e:
        print(f"Deu errado {e}")

# 1. Listar todos os cursos oferecidos por um determinado departamento
def questao1():
    try:
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
        print(sectionsMongo)
        for section in sectionsMongo:
            print(f'Course ID: {section["course_id"]}\tSection ID: {section["sec_id"]}\tSemester: {section["semester"]}\tYear: {section["year"]}\tBuilding: {section["building"]}\tRoom Number: {section["room_number"]}\tTime Slot ID: {section["time_slot_id"]}')
    except Exception as e:
        print(f'Deu ruim: {e}')

# questao1()
questao2("BIO-101", "Summer")