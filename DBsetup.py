import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import random
import json
from azure.cosmos import CosmosClient
import uuid

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

async def main():
    # Set up IoT Hub connection
    CONNECTION_STRING = os.getenv("DEVICE_CONNECTION_STRING")
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    await device_client.connect()

    # Set up Cosmos DB connection
    COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
    COSMOS_KEY = os.getenv("COSMOS_KEY")
    COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
    COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME")
    cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    cosmos_database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
    cosmos_container = cosmos_database.get_container_client(COSMOS_CONTAINER_NAME)

    async def send_telemetry(worker_type, worker_id):
        while True:
            # Simulate data for manual workers
            if worker_type == "manual_worker":
                # simulate vital signs and stress levels based on forklift availability and temperature
                # update this logic to simulate other stress factors that manual workers may face
                motion = random.choice(["walking", "lifting", "stretching"])
                posture = random.choice(["good", "bad"])
                payload = {
                    "worker_id": worker_id,
                    "heart_rate": random.randint(60, 100),
                    "skin_temperature": round(random.uniform(89, 95), 1),
                    "steps": random.randint(0, 100),
                    "motion": motion,
                    "posture": posture,
                    "motion_encoding":MOTION_ENCODING[motion],
                    "posture_encoding": POSTURE_ENCODING[posture],
                    "stress_level": random.randint(NONE_STRESS_LEVEL, HIGH_STRESS_LEVEL)
                }

            # Simulate data for forklift operators
            elif worker_type == "forklift_operator":
                # simulate stress levels based on forklift load and weight distribution
                # update this logic to simulate other stress factors that forklift operators may face
                forklift_status = random.choice(["idle", "moving", "loading", "unloading"])
                payload = {
                    "worker_id": worker_id,
                    "forklift_status": forklift_status,
                    "forklift_load": random.randint(0, 100),
                    "weight_distribution": random.choice(["even", "uneven"]),
                    "forklift_status_encoding": FORKLIFT_STATUS_ENCODING[forklift_status],
                    "stress_level": random.randint(NONE_STRESS_LEVEL, HIGH_STRESS_LEVEL)
                }

            # Simulate data for inventory managers
            elif worker_type == "inventory_manager":
                # simulate stress levels based on temperature and humidity
                # update this logic to simulate other stress factors that inventory managers may face
                payload = {
                    "worker_id": worker_id,
                    "inventory_level": random.randint(0, 100),
                    "temperature": round(random.uniform(60, 80), 1),
                    "humidity": random.randint(0, 100),
                    "stress_level": random.randint(NONE_STRESS_LEVEL, HIGH_STRESS_LEVEL)
                }

            # Simulate data for maintenance technicians
            else:
                # simulate stress levels based on machine status and performance
                # update this logic to simulate other stress factors that maintenance technicians may face
                maintenance_task = random.choice(["cleaning", "lubrication", "repair"])
                payload = {
                    "worker_id": worker_id,
                    "machine_status": random.choice(["idle", "running", "maintenance"]),
                    "machine_performance": random.choice(["good", "bad", "warning"]),
                    "maintenance_task": maintenance_task,
                    "maintenance_task_encoding": MAINTENANCE_TASK_ENCODING[maintenance_task],
                    "stress_level": random.randint(NONE_STRESS_LEVEL, HIGH_STRESS_LEVEL)
                }

            # Generate a unique identifier for the payload
            payload_id = str(uuid.uuid4())

            # Add the id property to the payload
            payload["id"] = payload_id

            print(f"Sending payload for {worker_type} {worker_id}: {payload}")

            # Serialize payload as a JSON document
            json_payload = json.dumps(payload)

            # Create a message from the JSON payload
            message = Message(json_payload)
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            # Send the message to IoT Hub
            await device_client.send_message(message)

            # Insert the payload into Cosmos DB
            cosmos_container.create_item(body=payload)

            # Wait for 60 seconds before sending the next message
            await asyncio.sleep(60)
            
    # Start tasks for each worker
    tasks = []
    for i in range(1, 6):
        tasks.append(asyncio.create_task(send_telemetry("manual_worker", f"MW{i}")))
    for i in range(1, 4):
        tasks.append(asyncio.create_task(send_telemetry("forklift_operator", f"FO{i}")))
    for i in range(1, 3):
        tasks.append(asyncio.create_task(send_telemetry("inventory_manager", f"IM{i}")))
    for i in range(1, 3):
        tasks.append(asyncio.create_task(send_telemetry("maintenance_technician", f"MT{i}")))

    await asyncio.gather(*tasks)

    # Disconnect from IoT Hub
    await device_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())