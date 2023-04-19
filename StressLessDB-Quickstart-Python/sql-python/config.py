import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://stressless-db01.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'c4vuHkyKfDNZicoLcAyLwNA87jpgKDLuZCNANURi4IYO6gJHiBNG4wPcVGNGCfT2lFZHMrOJ0fAIACDbtPvNjQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ToDoList'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}