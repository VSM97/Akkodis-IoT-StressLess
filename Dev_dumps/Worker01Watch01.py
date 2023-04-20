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

    async def send_telemetry():
        while True:
            heart_rate = random.randint(60, 100)
            skin_temperature = round(random.uniform(89, 95), 1)
            steps = random.randint(0, 100)

            payload = {
                "heartRate": heart_rate,
                "skinTemperature": skin_temperature,
                "steps": steps
            }

            message = Message(json.dumps(payload))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            await device_client.send_message(message)
            await asyncio.sleep(60)

    await send_telemetry()

    await device_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
