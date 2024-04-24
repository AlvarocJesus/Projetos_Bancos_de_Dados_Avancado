# pip --version
# python -m pip install --upgrade pip
# pip install astrapy
from astrapy import DataAPIClient

astraToken = 'AstraCS:qpZoBwBqvCQnRmmEjepXexYq:36634fa9375d6c56bd8ccecc333f090f2af51ebb9635161eba0df732966a7b27'

# Initialize the client
client = DataAPIClient(f"{astraToken}")
db = client.get_database_by_api_endpoint(
  "https://249f483f-685e-4b8a-8436-ae34dd6f7103-us-east-2.apps.astra.datastax.com"
)

print(f"Connected to Astra DB: {db.list_collection_names()}")

