import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
  os.getenv("NEO4J_URI"),
  auth = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

connection = driver.verify_connectivity()
print(f'Conectado ao Neo4j: {connection}')

session = driver.session()
print(f'Sessão criada: {session}')

