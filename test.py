import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
import numpy as np
from azure.cosmos import CosmosClient

# Declare stress level constants
NONE_STRESS_LEVEL = 0
LOW_STRESS_LEVEL = 1
MEDIUM_STRESS_LEVEL = 2
HIGH_STRESS_LEVEL = 3

# Define one-hot encoding dictionaries for categorical variables
MOTION_ENCODING = {"walking": [1, 0, 0], "lifting": [0, 1, 0], "stretching": [0, 0, 1]}
POSTURE_ENCODING = {"good": [1, 0], "bad": [0, 1]}
FORKLIFT_STATUS_ENCODING = {"idle": [1, 0, 0, 0], "moving": [0, 1, 0, 0], "loading": [0, 0, 1, 0], "unloading": [0, 0, 0, 1]}
MAINTENANCE_TASK_ENCODING = {"cleaning": [1, 0, 0], "lubrication": [0, 1, 0], "repair": [0, 0, 1]}

# Set up IoT Hub connection
CONNECTION_STRING = os.getenv("DEVICE_CONNECTION_STRING")
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
device_client.connect()

# Set up Cosmos DB connection
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME")
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
cosmos_database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
cosmos_container = cosmos_database.get_container_client(COSMOS_CONTAINER_NAME)

# Query data from Cosmos DB
query = "SELECT * FROM c WHERE c.Processed = false"
items = list(cosmos_container.query_items(
    query=query,
    enable_cross_partition_query=True
))

if len(items) > 0:
    # Convert data to pandas dataframe
    df = pd.DataFrame(items)

    # Identify variables to be excluded from one-hot encoding
    exclude_vars = ['worker_id','id',"_rid","_self","_etag","_attachments","_ts", 'Processed']

    # Convert categorical variables to strings
    categorical_vars = [col for col in df.columns if col not in exclude_vars and not pd.api.types.is_numeric_dtype(df[col])]
    df[categorical_vars] = df[categorical_vars].astype(str)

    # One-hot encode categorical variables
    enc = OneHotEncoder(handle_unknown='ignore')
    for col in ['motion', 'posture', 'forklift_status', 'maintenance_task']:
        if col in df.columns:
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

    X = imp.fit_transform(df.drop(['worker_id', 'id', "_rid", "_self", "_etag", "_attachments", "_ts", 'stress_level_none', 'Processed'], axis=1))
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

async def send_telemetry(worker_type, worker_id):
    while True:
        # Query data from Cosmos DB
        query = f"SELECT * FROM c WHERE c.worker_id = '{worker_id}' AND c.Processed = false"
        items = list(cosmos_container.query_items(
            query=query,
            enable_cross_partition_query=True))

        # Make predictions and send recommendations for each unprocessed document
        for item in items:
            # Set the 'Processed' field to True
            item['Processed'] = True
            cosmos_container.replace_item(item=item, item_id=item['id'], partition_key=item['worker_id'])

            # Make a prediction using the trained model
            worker_df = pd.DataFrame([item])
            worker_df[categorical_vars] = worker_df[categorical_vars].astype(str)
            for col in ['motion', 'posture', 'forklift_status', 'maintenance_task']:
                if col in worker_df.columns:
                    enc_df = pd.DataFrame(enc.transform(worker_df[[col]]).toarray(), columns=[f"{col}_{cat}" for cat in enc.categories_[0]])
                    worker_df = pd.concat([worker_df, enc_df], axis=1)
            worker_df = worker_df.drop(categorical_vars, axis=1)
            worker_X_imputed = imp.transform(worker_df.drop(['worker_id', 'id', "_rid", "_self", "_etag", "_attachments", "_ts", 'stress_level_none', 'Processed'], axis=1))
            worker_X_imputed_df = pd.DataFrame(worker_X_imputed, columns=[f"feature_{i}" for i in range(worker_X_imputed.shape[1])])
            predicted_stress_level = rfc.predict(worker_X_imputed_df)

            # Provide personalized training recommendations based on job role
            if worker_type == 'Maintenance Worker':
                if predicted_stress_level[0] == NONE_STRESS_LEVEL:
                    training_recommendation = "Your stress level is none. Keep up the good work and stay safe!"
                elif predicted_stress_level[0] == LOW_STRESS_LEVEL:
                    training_recommendation = "Your stress level is low. Continue with your regular training."
                elif predicted_stress_level[0] == MEDIUM_STRESS_LEVEL:
                    training_recommendation = "Your stress level is medium. We recommend taking additional training on stress management."
                else:
                    training_recommendation = "Your stress level is high. We recommend taking additional training on stress management and seeking medical attention if necessary."
            elif worker_type == 'Forklift Operator':
                if predicted_stress_level[0] == NONE_STRESS_LEVEL:
                    training_recommendation = "Your stress level is none. Keep up the good work and stay safe!"
                elif predicted_stress_level[0] == LOW_STRESS_LEVEL:
                    training_recommendation = "Your stress level is low. Continue with your regular training."
                elif predicted_stress_level[0] == MEDIUM_STRESS_LEVEL:
                    training_recommendation = "Your stress level is medium. We recommend taking additional training on stress management and proper forklift operation."
                else:
                    training_recommendation = "Your stress level is high. We recommend taking additional training on stress management, proper forklift operation, and seeking medical attention if necessary."
            elif worker_type == 'Inventory Manager':
                if predicted_stress_level[0] == NONE_STRESS_LEVEL:
                    training_recommendation = "Your stress level is none. Keep up the good work and stay safe!"
                elif predicted_stress_level[0] == LOW_STRESS_LEVEL:
                    training_recommendation = "Your stress level is low. Continue with your regular tasks, but remember to take breaks and stay hydrated."
                elif predicted_stress_level[0] == MEDIUM_STRESS_LEVEL:
                    training_recommendation = "Your stress level is medium. We recommend taking additional training on stress management and time management."
                else:
                    training_recommendation = "Your stress level is high. We recommend taking additional training on stress management, time management, and seeking medical attention if necessary."
            else:
                training_recommendation = "Training recommendations not available for this job role."

            # Send telemetry to IoT Hub
            telemetry_data = {
                "worker_id": item["worker_id"],
                "stress_level": predicted_stress_level[0],
                "training_recommendation": training_recommendation
            }
            telemetry_json = json.dumps(telemetry_data)
            message = Message(telemetry_json)
            await device_client.send_message(message)
            print(f"Sent telemetry data for worker {worker_id}: {telemetry_json}")

        # Wait for 60 seconds before checking for new data
        await asyncio.sleep(60)


# Start sending telemetry for each worker
worker_types = ["Maintenance Worker", "Forklift Operator", "Inventory Manager"]
worker_ids = ["worker1", "worker2", "worker3"]
for worker_type, worker_id in zip(worker_types, worker_ids):
    asyncio.run(send_telemetry(worker_type, worker_id))