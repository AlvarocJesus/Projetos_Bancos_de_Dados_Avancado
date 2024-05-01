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

def create_person(tx, name):
  tx.run("CREATE (a:Person {name: $name})", name=name)

create_person(session, "Alice")

