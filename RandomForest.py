import os
from azure.cosmos import CosmosClient
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
import numpy as np

# Set up Cosmos DB connection
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME")
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
cosmos_database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
cosmos_container = cosmos_database.get_container_client(COSMOS_CONTAINER_NAME)

# Query data from Cosmos DB
query = "SELECT * FROM c"
items = list(cosmos_container.query_items(
    query=query,
    enable_cross_partition_query=True
))

# Convert data to pandas dataframe
df = pd.DataFrame(items)

# Identify variables to be excluded from one-hot encoding
exclude_vars = ['worker_id', 'id',"_rid","_self","_etag","_attachments","_ts"]

# Convert categorical variables to strings
categorical_vars = [col for col in df.columns if col not in exclude_vars and not pd.api.types.is_numeric_dtype(df[col])]
df[categorical_vars] = df[categorical_vars].astype(str)

# One-hot encode categorical variables
enc = OneHotEncoder(handle_unknown='ignore')
for col in ['stress_level']:
    enc_df = pd.DataFrame(enc.fit_transform(df[[col]]).toarray(), columns=[f"{col}_{cat}" for cat in enc.categories_[0]])
    df = pd.concat([df, enc_df], axis=1)

# Drop original categorical variables
df = df.drop(categorical_vars, axis=1)

# Fill in missing values with different imputation strategies
# Choose one of the following strategies: 'mean', 'median', 'mode', 'knn', 'iterative'
imputation_strategy = 'knn'

if imputation_strategy == 'mean':
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
elif imputation_strategy == 'median':
    imp = SimpleImputer(missing_values=np.nan, strategy='median')
elif imputation_strategy == 'mode':
    imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
elif imputation_strategy == 'knn':
    imp = KNNImputer(n_neighbors=5, weights='uniform')
elif imputation_strategy == 'iterative':
    imp = IterativeImputer(max_iter=10, random_state=42)

X = imp.fit_transform(df.drop(['worker_id', 'id', "_rid", "_self", "_etag", "_attachments", "_ts", 'stress_level_none'], axis=1))
y = df['stress_level_none']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Fit Random Forest classifier
rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)

# Evaluate model
score = rfc.score(X_test, y_test)
print(f"Model accuracy: {score}")
