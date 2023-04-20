# StressLess IoT

StressLess is an IoT product aimed at monitoring workers' physiological stress levels in real-time to improve their performance and reduce the risk of injury. The system collects biometric data from workers, analyzes the data to determine stress levels, and provides customized training recommendations based on the workers' physiological stress levels.

## Table of Contents

- [StressLess IoT](#stressless-iot)
  - [Table of Contents](#table-of-contents)
  - [Database Structure](#database-structure)
  - [System Overview](#system-overview)
  - [Initial Setup](#initial-setup)
    - [Execution Order](#execution-order)
  - [Model Training and Predictions](#model-training-and-predictions)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Database Structure

The database contains records for the following worker types:

- Manual Workers (MW)
- Forklift Operators (FO)
- Inventory Managers (IM)
- Maintenance Technicians (MT)

Worker IDs are represented as follows:

- MW1 - Manual Worker 01
- MW2 - Manual Worker 02
- MW3 - Manual Worker 03
- MW4 - Manual Worker 04
- MW5 - Manual Worker 05
- ...
- FO1 - Forklift Operator 01
- FO2 - Forklift Operator 02
- FO3 - Forklift Operator 03
- ...
- IM1 - Inventory Manager 01
- IM2 - Inventory Manager 02
- ...
- MT1 - Maintenance Technician 01
- MT2 - Maintenance Technician 02

## System Overview

The system consists of the following main components:

1. IoT devices to collect biometric data from workers
2. Azure IoT Hub to securely manage and transfer the data
3. Azure Cosmos DB to store the collected data
4. A machine learning model to analyze the data and predict stress levels
5. A user-friendly interface to display the training recommendations

## Initial Setup

Before running the main scripts, ensure that all the documents in the Cosmos DB have their "Processed" flag set to `false`. This allows the RandomForest algorithm to start with a clean state and set the flag to `true` when the model has been trained.

### Execution Order

To achieve optimal results, execute the scripts in the following order:

1. `01_reset_processed_flag.py` - Set the "Processed" flag to `false` for all documents in Cosmos DB.
2. `02_send_telemetry_to_cosmosdb.py` - Sends biometric/telemetry data to Cosmos DB.
3. `03_stress_detection_and_recommendations.py` - Contains the RandomForestClassifier model to detect stress levels and the recommendation algorithm to send responses to the IoT Hub for workers to access.

By following this order, you ensure that the system is properly set up and the RandomForest model can accurately detect stress levels and provide appropriate training recommendations.

## Model Training and Predictions

The RandomForest model is initially trained using data with the "Processed" flag set to `false`. Once the model is trained, the system directly performs predictions on any new incoming data without updating the model. The "Processed" flag is not changed for the new data, and it is used only for making predictions.

To control whether the model should be retrained with new data or not, a variable named `model_trained` is introduced in the `03_stress_detection_and_recommendations.py` script. This variable tracks whether the model has already been trained or not. Once the model has been trained using the initial data with the "Processed" flag set to `false`, the variable will be updated, and the model will not be retrained with the new incoming data.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/VSM97/Akkodis-IOT-StressLess.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables for the Azure IoT Hub and Azure Cosmos DB:

    ```bash
    export DEVICE_CONNECTION_STRING=<your_device_connection_string>
    export COSMOS_ENDPOINT=<your_cosmos_db_endpoint>
    export COSMOS_KEY=<your_cosmos_db_key>
    export COSMOS_DATABASE_NAME=<your_cosmos_db_database_name>
    export COSMOS_CONTAINER_NAME=<your_cosmos_db_container_name>
    ```

## Usage

1. If there is already data in the Cosmos DB, run the script to reset the "Processed" flag:

    ```bash
    python 01_reset_processed_flag.py
    ```

2. Run the IoT device simulator script:

    ```bash
    python 02_send_telemetry_to_cosmosdb.py
    ```

3. Run the main analysis and recommendation script:

    ```bash
    python 03_stress_detection_and_recommendations.py
    ```

The system will start collecting data from the simulated IoT devices, analyze the data, and provide training recommendations based on the workers' physiological stress levels.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is a property of Akkodis and its usage is prohibited without explicit permission. For inquiries and usage permissions, please contact Akkodis. Unauthorized use or distribution of this project may result in legal consequences.
