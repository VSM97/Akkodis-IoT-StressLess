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

# Set valid feature names to X_train
X_train = pd.DataFrame(X_train, columns=[f"feature_{i}" for i in range(X_train.shape[1])])

# Fit Random Forest classifier
rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)

# Evaluate model
score = rfc.score(X_test, y_test)
print(f"Accuracy: {score:.2f}")

for worker_id in ['MW1', 'MW2', 'MW3', 'MW4', 'MW5', 'FO1', 'FO2', 'FO3', 'IM1', 'IM2', 'MT1', 'MT2']:
    worker_df = df[df['worker_id'] == worker_id].drop(['worker_id', 'id', "_rid", "_self", "_etag", "_attachments", "_ts", 'stress_level_none'], axis=1)

    if not worker_df.empty:
        worker_X_imputed = imp.transform(worker_df)

        # Set valid feature names to worker_X_imputed_df
        worker_X_imputed_df = pd.DataFrame(worker_X_imputed, columns=[f"feature_{i}" for i in range(worker_X_imputed.shape[1])])

        # Make predictions for the worker
        predicted_stress_level = rfc.predict(worker_X_imputed_df)

        # Provide personalized training recommendations based on job role
        if worker_id.startswith('MW'):
            # Training recommendations for Maintenance Workers
            if predicted_stress_level[0] == 0:
                training_recommendation = "Your stress level is none. Keep up the good work and continue with your regular training routine. Consider adding stretching exercises to your routine to improve flexibility and prevent injuries."
            elif predicted_stress_level[0] == 1:
                training_recommendation = "Your stress level is low. Continue with your regular training routine. Consider adding stretching and cardiovascular exercises to your routine to improve endurance and prevent injuries."
            elif predicted_stress_level[0] == 2:
                training_recommendation = "Your stress level is medium. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve muscular endurance and strength, and include rest days in your routine to allow for recovery. Consider adding exercises that improve balance and coordination, as these skills are important for performing tasks safely and efficiently."
            else:
                training_recommendation = "Your stress level is high. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve muscular endurance and strength, and include rest days in your routine to allow for recovery. Consider adding exercises that improve balance and coordination, as these skills are important for performing tasks safely and efficiently."

        elif worker_id.startswith('FO'):
            # Training recommendations for Forklift Operators
            if predicted_stress_level[0] == 0:
                training_recommendation = "Your stress level is none. Keep up the good work and continue with your regular training routine. Consider adding cardio exercises to your routine to improve cardiovascular health."
            elif predicted_stress_level[0] == 1:
                training_recommendation = "Your stress level is low. Continue with your regular training routine. Consider adding cardio exercises and stretching to your routine to improve cardiovascular health and prevent injuries."
            elif predicted_stress_level[0] == 2:
                training_recommendation = "Your stress level is medium. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve flexibility and mobility, and include rest days in your routine to allow for recovery. Consider adding exercises that improve core strength and posture, as these skills are important for maintaining a healthy spine and preventing back pain."
            else:
                training_recommendation = "Your stress level is high. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve flexibility and mobility, and include rest days in your routine to allow for recovery. Consider adding exercises that improve core strength and posture, as these skills are important for maintaining a healthy spine and preventing back pain."

        elif worker_id.startswith('IM'):
            # Training recommendations for Inventory Managers
            if predicted_stress_level[0] == 0:
                training_recommendation = "Your stress level is none. Keep up the good work and continue with your regular training routine. Consider adding exercises that improve upper body strength and posture to maintain good health and prevent injuries."
            elif predicted_stress_level[0] == 1:
                training_recommendation = "Your stress level is low. Continue with your regular training routine. Consider adding exercises that improve upper body strength and posture to maintain good health and prevent injuries."
            elif predicted_stress_level[0] == 2:
                training_recommendation = "Your stress level is medium. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve lower body strength and flexibility, and include rest days in your routine to allow for recovery. Consider adding exercises that improve balance and coordination, as these skills are important for maintaining stability and preventing falls."
            else:
                training_recommendation = "Your stress level is high. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve lower body strength and flexibility, and include rest days in your routine to allow for recovery. Consider adding exercises that improve balance and coordination, as these skills are important for maintaining stability and preventing falls."

        elif worker_id.startswith('MT'):
            # Training recommendations for Maintenance Technicians
            if predicted_stress_level[0] == 0:
                training_recommendation = "Your stress level is none. Keep up the good work and continue with your regular training routine. Consider adding exercises that improve flexibility and core strength to maintain good health and prevent injuries."
            elif predicted_stress_level[0] == 1:
                training_recommendation = "Your stress level is low. Continue with your regular training routine. Consider adding exercises that improve flexibility and core strength to maintain good health and prevent injuries."
            elif predicted_stress_level[0] == 2:
                training_recommendation = "Your stress level is medium. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve muscular endurance and strength, and include rest days in your routine to allow for recovery. Consider adding exercises that improve balance and coordination, as these skills are important for performing tasks safely and efficiently. Additionally, consider adding exercises that improve grip strength, as this is important for performing tasks that require gripping tools and equipment."
            else:
                training_recommendation = "Your stress level is high. We recommend modifying your training routine to reduce stress and prevent injuries. Focus on exercises that improve muscular endurance and strength, and include rest days in your routine to allow for recovery. Consider adding exercises that improve balance and coordination, as these skills are important for performing tasks safely and efficiently. Additionally, consider adding exercises that improve grip strength, as this is important for performing tasks that require gripping tools and equipment."

        print(f"Training recommendation for worker {worker_id}: {training_recommendation}")
    else:
        print(f"Worker with ID {worker_id} not found in the dataset.")