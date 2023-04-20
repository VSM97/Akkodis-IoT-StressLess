# Akkodis-IOT-StressLess
 StressLess IOT product to monitor workers physiological stress

Database structure

MW1- manual_worker 01
MW2- manual_worker 02
MW3- manual_worker 03
MW4- manual_worker 04
MW5- manual_worker 05
FO1- forklift_operator 01
FO2- forklift_operator 02
FO3- forklift_operator 03
IM1- inventory_manager 01
IM2- inventory_manager 02
MT1- maintenance_technician 01
MT2- maintenance_technician 02

Actual CosmosDB content:

{
        "worker_id": "MW1",
        "heart_rate": 91,
        "skin_temperature": 90,
        "steps": 58,
        "motion": "stretching",
        "posture": "bad",
        "motion_encoding": [
            0,
            0,
            1
        ],
        "posture_encoding": [
            0,
            1
        ],
        "stress_level": 3,
        "id": "7c9a5888-007b-4130-a51f-c50ca1ea5076",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ2CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ2CwAAAAAAAA==/",
        "_etag": "\"3900512a-0000-0700-0000-6440a28c0000\"",
        "_attachments": "attachments/",
        "_ts": 1681957516
    },
    {
        "worker_id": "MW2",
        "heart_rate": 85,
        "skin_temperature": 91.4,
        "steps": 19,
        "motion": "stretching",
        "posture": "bad",
        "motion_encoding": [
            0,
            0,
            1
        ],
        "posture_encoding": [
            0,
            1
        ],
        "stress_level": 2,
        "id": "7b7b2100-f7be-43fc-836e-3a41e2ffb901",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ3CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ3CwAAAAAAAA==/",
        "_etag": "\"3900522a-0000-0700-0000-6440a28d0000\"",
        "_attachments": "attachments/",
        "_ts": 1681957517
    },
    {
        "worker_id": "MW3",
        "heart_rate": 68,
        "skin_temperature": 94.1,
        "steps": 52,
        "motion": "lifting",
        "posture": "bad",
        "motion_encoding": [
            0,
            1,
            0
        ],
        "posture_encoding": [
            0,
            1
        ],
        "stress_level": 3,
        "id": "0a324db4-93f6-4897-90e1-763c80f8c261",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ4CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ4CwAAAAAAAA==/",
        "_etag": "\"39006f2a-0000-0700-0000-6440a28e0000\"",
        "_attachments": "attachments/",
        "_ts": 1681957518
    },
    {
        "worker_id": "MW4",
        "heart_rate": 98,
        "skin_temperature": 90.3,
        "steps": 43,
        "motion": "walking",
        "posture": "bad",
        "motion_encoding": [
            1,
            0,
            0
        ],
        "posture_encoding": [
            0,
            1
        ],
        "stress_level": 0,
        "id": "33fcf4d6-bf86-4e03-ae97-befa3c3501a6",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ5CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ5CwAAAAAAAA==/",
        "_etag": "\"3900ad2a-0000-0700-0000-6440a2900000\"",
        "_attachments": "attachments/",
        "_ts": 1681957520
    },
    {
        "worker_id": "MW5",
        "heart_rate": 69,
        "skin_temperature": 90.8,
        "steps": 25,
        "motion": "walking",
        "posture": "good",
        "motion_encoding": [
            1,
            0,
            0
        ],
        "posture_encoding": [
            1,
            0
        ],
        "stress_level": 0,
        "id": "3636e9d3-0a0c-4c81-a3ce-af04c7cffa3d",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ6CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ6CwAAAAAAAA==/",
        "_etag": "\"3900f62a-0000-0700-0000-6440a2900000\"",
        "_attachments": "attachments/",
        "_ts": 1681957520
    },
    {
        "worker_id": "FO1",
        "forklift_status": "loading",
        "forklift_load": 50,
        "weight_distribution": "even",
        "forklift_status_encoding": [
            0,
            0,
            1,
            0
        ],
        "stress_level": 0,
        "id": "70717fe8-aad2-4e4d-8f8d-bae83c942bec",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ7CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ7CwAAAAAAAA==/",
        "_etag": "\"3900102b-0000-0700-0000-6440a2910000\"",
        "_attachments": "attachments/",
        "_ts": 1681957521
    },
    {
        "worker_id": "FO2",
        "forklift_status": "idle",
        "forklift_load": 77,
        "weight_distribution": "even",
        "forklift_status_encoding": [
            1,
            0,
            0,
            0
        ],
        "stress_level": 2,
        "id": "8a324f4d-2b45-499e-b62a-cc1fd5a669c2",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ8CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ8CwAAAAAAAA==/",
        "_etag": "\"3900112b-0000-0700-0000-6440a2910000\"",
        "_attachments": "attachments/",
        "_ts": 1681957521
    },
    {
        "worker_id": "FO3",
        "forklift_status": "loading",
        "forklift_load": 78,
        "weight_distribution": "uneven",
        "forklift_status_encoding": [
            0,
            0,
            1,
            0
        ],
        "stress_level": 3,
        "id": "40bb106f-771c-4b41-b284-cf1bcd2bd81b",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ9CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ9CwAAAAAAAA==/",
        "_etag": "\"39003a2b-0000-0700-0000-6440a2920000\"",
        "_attachments": "attachments/",
        "_ts": 1681957522
    },
    {
        "worker_id": "IM1",
        "inventory_level": 96,
        "temperature": 78.5,
        "humidity": 62,
        "stress_level": 3,
        "id": "65eed4d2-d71c-49c5-9311-5d492bda8dfa",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ+CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ+CwAAAAAAAA==/",
        "_etag": "\"3900772b-0000-0700-0000-6440a2940000\"",
        "_attachments": "attachments/",
        "_ts": 1681957524
    },
    {
        "worker_id": "IM2",
        "inventory_level": 58,
        "temperature": 70.6,
        "humidity": 45,
        "stress_level": 0,
        "id": "ba9e1ad8-c3ad-4e2d-8383-2d2a88ab6679",
        "Processed": false,
        "_rid": "-UdLAPY-4YZ-CwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YZ-CwAAAAAAAA==/",
        "_etag": "\"3900a72b-0000-0700-0000-6440a2950000\"",
        "_attachments": "attachments/",
        "_ts": 1681957525
    },
    {
        "worker_id": "MT1",
        "machine_status": "running",
        "machine_performance": "good",
        "maintenance_task": "cleaning",
        "maintenance_task_encoding": [
            1,
            0,
            0
        ],
        "stress_level": 0,
        "id": "83baea6a-53ae-4cc0-9abc-43b700744116",
        "Processed": false,
        "_rid": "-UdLAPY-4YaACwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YaACwAAAAAAAA==/",
        "_etag": "\"3900ba2b-0000-0700-0000-6440a2960000\"",
        "_attachments": "attachments/",
        "_ts": 1681957526
    },
    {
        "worker_id": "MT2",
        "machine_status": "idle",
        "machine_performance": "bad",
        "maintenance_task": "cleaning",
        "maintenance_task_encoding": [
            1,
            0,
            0
        ],
        "stress_level": 1,
        "id": "b6fcbff9-5c15-4ac4-ae35-2c264865fbfc",
        "Processed": false,
        "_rid": "-UdLAPY-4YaBCwAAAAAAAA==",
        "_self": "dbs/-UdLAA==/colls/-UdLAPY-4YY=/docs/-UdLAPY-4YaBCwAAAAAAAA==/",
        "_etag": "\"3900cf2b-0000-0700-0000-6440a2970000\"",
        "_attachments": "attachments/",
        "_ts": 1681957527
    }