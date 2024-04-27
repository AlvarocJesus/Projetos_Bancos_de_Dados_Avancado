from astrapy import DataAPIClient
from configparser import ConfigParser

config = ConfigParser().read('../config.ini')
# print(config.get("ASTRADB","astraURL"))

# Initialize the client
client = DataAPIClient(config["ASTRADB"]["astraToken"])
db = client.get_database_by_api_endpoint(
  config["ASTRADB"]["astraURL"],
)

print(f"Connected to Astra DB: {db.list_collection_names()}")

