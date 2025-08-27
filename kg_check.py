from dotenv import load_dotenv
import os
from langchain_neo4j import Neo4jGraph
import importlib
import os

# Load Neo4j credentials from .env
load_dotenv()
NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

# Connect to Neo4j
kg = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

# Path to folder with chapter_*.py files
CYPHER_QUERY_FOLDER = "cypher_queries"

def run_all_chapters():
    for filename in sorted(os.listdir(CYPHER_QUERY_FOLDER)):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # remove .py
            module_path = f"{CYPHER_QUERY_FOLDER}.{module_name}"

            try:
                print(f"🚀 Running {filename} ...")
                mod = importlib.import_module(module_path)
                kg.query(mod.cypher)
                print(f"✅ Finished {filename}\n")
            except Exception as e:
                print(f"❌ Error in {filename}: {e}\n")

if __name__ == "__main__":
    run_all_chapters()


#
# from dotenv import load_dotenv
# import os
# from langchain_neo4j import Neo4jGraph #GraphCypherQAChain
# # from langchain_community.graphs import Neo4jGraph
#
# load_dotenv()
#
# AURA_INSTANCENAME = os.environ["AURA_INSTANCENAME"]
# NEO4J_URI = os.environ["NEO4J_URI"]
# NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
# NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
# AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)
#
#
# kg = Neo4jGraph(
#     url=NEO4J_URI,
#     username=NEO4J_USERNAME,
#     password=NEO4J_PASSWORD,
# ) # database=NEO4J_DATABASE,
#
# cypher = """
#   MATCH (n)
#   RETURN count(n) as numberOfNodes
#   """
#
# result = kg.query(cypher)
# print(f"There are {result[0]['numberOfNodes']} nodes in this graph.")
