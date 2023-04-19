from azure.cosmos import CosmosClient
import os

# Set up Cosmos DB connection
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME")
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
cosmos_database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
cosmos_container = cosmos_database.get_container_client(COSMOS_CONTAINER_NAME)

# Query all documents in the container
for item in cosmos_container.query_items(
    query="SELECT * FROM c",
    enable_cross_partition_query=True
):
    # Add the new field to the document
    item["Processed"] = "False"
    
    # Update the document in the container
    cosmos_container.upsert_item(item)