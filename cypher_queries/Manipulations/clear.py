import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

# Load environment variables
load_dotenv()

NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

# Connect to Neo4j
kg = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)

# Load the clear query
with open("clear.txt", "r", encoding="utf-8") as file:
    clear_query = file.read()

# Execute
try:
    print("🧹 Clearing Neo4j instance...")
    kg.query(clear_query)
    print("✅ All nodes and relationships deleted.")
except Exception as e:
    print(f"❌ Error during deletion: {e}")
