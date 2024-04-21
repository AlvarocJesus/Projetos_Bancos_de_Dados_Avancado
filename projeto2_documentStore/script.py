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

# 1. Listar todos os cursos oferecidos por um determinado departamento
def questao1():
    try:
        # busca no sql e insere no mongodb os cursos - OK
        cursos = getDataSQLDB('select * from course;')
        print('Cursos SQL')
        print(cursos)
        teste = db.course.insert_many(cursos)
        print('Cursos MongoDB')
        print(teste)
        print(f'inserted_ids: {teste.inserted_ids}')
        # busca no sql e insere no mongodb os departamentos
        """ departamentos = getDataSQLDB(
            select * from department d 
            inner join course c on d.dept_name = c.dept_name
            order by d.dept_name;
        )

        departamentosFormatado = []
        for departamento in range(len(departamentos)):
            print(departamentos[departamento])

            if departamentos[departamento] == cursos[departamento].dept_name:
                departamentosFormatado.append({
                    "dept_name": departamentos[departamento][0],
                    "building": departamentos[departamento][1],
                    "budget": departamentos[departamento][2],
                    "courses": [cursos[departamento]._id]
                })

        # db.course.insert_many(departamentosFormatado) """



        # departamento = db.department.find({}, { "_id": 0, "name": 1, "courses": 2 })
        # for depart in departamento:
        #     for cursoId in depart['courses']:
        #         cursos = db.course.find({ "_id": ObjectId(cursoId) }, { "_id": 0, "course_id": 1, "title": 2  })
        #         for curso in cursos:
        #             print(f'Departamento: {depart["name"]}\tID do curso: {curso["course_id"]}\tNome do curso: {curso["title"]}')
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