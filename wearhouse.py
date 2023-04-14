import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import random
import json

async def main():
    CONNECTION_STRING = os.getenv("DEVICE_CONNECTION_STRING")
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    await device_client.connect()

    async def send_telemetry(worker_type, worker_id):
        while True:
            # Simulate data for manual workers
            if worker_type == "manual_worker":
                # simulate vital signs and stress levels based on forklift availability and temperature
                # update this logic to simulate other stress factors that manual workers may face
                payload = {
                    "heartRate": random.randint(60, 100),
                    "skinTemperature": round(random.uniform(89, 95), 1),
                    "steps": random.randint(0, 100),
                    "motion": random.choice(["walking", "lifting", "stretching"]),
                    "posture": random.choice(["good", "bad"]),
                    "stressLevel": random.choice(["none", "low", "medium", "high"])
                }

            # Simulate data for forklift operators
            elif worker_type == "forklift_operator":
                # simulate stress levels based on forklift load and weight distribution
                # update this logic to simulate other stress factors that forklift operators may face
                payload = {
                    "forkliftStatus": random.choice(["idle", "moving", "loading", "unloading"]),
                    "forkliftLoad": random.randint(0, 100),
                    "weightDistribution": random.choice(["even", "uneven"]),
                    "stressLevel": random.choice(["none", "low", "medium", "high"])
                }

            # Simulate data for inventory managers
            elif worker_type == "inventory_manager":
                # simulate stress levels based on temperature and humidity
                # update this logic to simulate other stress factors that inventory managers may face
                payload = {
                    "inventoryLevel": random.randint(0, 100),
                    "temperature": round(random.uniform(60, 80), 1),
                    "humidity": random.randint(0, 100),
                    "stressLevel": random.choice(["none", "low", "medium", "high"])
                }

            # Simulate data for maintenance technicians
            else:
                # simulate stress levels based on machine status and performance
                # update this logic to simulate other stress factors that maintenance technicians may face
                payload = {
                    "machineStatus": random.choice(["idle", "running", "maintenance"]),
                    "machinePerformance": random.choice(["good", "bad", "warning"]),
                    "maintenanceTask": random.choice(["cleaning", "lubrication", "repair"]),
                    "stressLevel": random.choice(["none", "low", "medium", "high"])
                }

            print(f"Sending payload for {worker_type} {worker_id}: {payload}")

            message = Message(json.dumps(payload))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            await device_client.send_message(message)

            await asyncio.sleep(60)
            
    # Start tasks for each worker
    tasks = []
    for i in range(1, 6):
        tasks.append(asyncio.create_task(send_telemetry("manual_worker", f"0{i}")))
    for i in range(1, 4):
        tasks.append(asyncio.create_task(send_telemetry("forklift_operator", f"0{i}")))
    for i in range(1, 3):
        tasks.append(asyncio.create_task(send_telemetry("inventory_manager", f"0{i}")))
    for i in range(1, 3):
        tasks.append(asyncio.create_task(send_telemetry("maintenance_technician", f"0{i}")))

    await asyncio.gather(*tasks)

    await device_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
