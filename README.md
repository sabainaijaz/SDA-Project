# SDA-Project: Data-Driven Pipeline Analysis

## Description

This project implements a modular, data-driven pipeline processing system using:

* Functional programming style
* Single Responsibility Principle (SRP)
* Multiprocessing for concurrent workers
* Observer pattern for telemetry monitoring
* Configuration-driven behavior

The system reads metric or sensor data from a CSV file, generates security hashes for verification, processes data concurrently using worker processes, aggregates results using a sliding window, and displays real-time dashboards and queue telemetry.

## Project Architecture

Follows a layered and modular design:

```
project_root/
│
├── main.py                     # Entry point (Orchestrator)
├── config.json                 # Configuration file
├── data/                       # Input CSV files
│   └── sample_sensor_data.csv
├── core/
│   ├── __init__.py
│   ├── functional.py           # Pure functional operations
│   ├── worker.py               # Worker process for validation
│   ├── aggregator.py           # Aggregator process with sliding window
│   └── telemetry.py            # Pipeline telemetry class
├── input.py                     # Reads CSV, converts types, computes hash
├── output/
│   ├── dashboard.py            # Live value & running average dashboard
│   └── telemtry_view.py        # Queue telemetry visualization
├── monitor.py                  # Observer pattern implementation
└── crypto.py                   # PBKDF2 HMAC SHA-256 signature generation
```

## Features and Analysis Supported

1. Reads metric/sensor data from any CSV file.
2. Converts column types dynamically based on `config.json`.
3. Generates security hashes for each metric value for verification.
4. Concurrently validates data using worker processes.
5. Aggregates values using sliding window to compute running averages.
6. Displays live dashboards for raw and processed values.
7. Monitors queue sizes in real-time using Observer pattern and telemetry view.
8. Fully configuration-driven system for flexibility.

## Configuration

Example configuration structure:

```json
{
    "file": "data/sample_sensor_data.csv",
    "columns": [
        {"from": "Timestamp", "to": "time", "type": "integer"},
        {"from": "Raw_Value", "to": "value", "type": "float"},
        {"from": "Sensor_ID", "to": "entity", "type": "string"}
    ],
    "speed": {
        "input_delay": 0.01,
        "workers": 4,
        "queue_size": 50
    },
    "security": {
        "key": "my_secret_key",
        "iterations": 100000
    },
    "processing": {
        "window_size": 10
    },
    "display": {
        "show_raw": true,
        "show_processed": true
    }
}
```

## Design Principles Used

* **Single Responsibility Principle (SRP)**

  * Each module has one responsibility: Input, Worker, Aggregator, Dashboard, Telemetry.
* **Functional Programming Style**

  * Uses pure functions: `verify_signature`, `running_average`, `filter_verified`.
  * Avoids explicit loops using `map`, `filter`, `lambda`.
* **Observer Pattern for Telemetry**

  * Monitor observes pipeline queues and notifies telemetry view.
* **Multiprocessing / Concurrency**

  * Input, Worker, Aggregator, Dashboard, and Monitor run in separate processes.
* **Configuration-Driven**

  * Behavior is driven entirely by `config.json`.

## How to Run

1. Ensure `config.json` and CSV data files are present.
2. Install required libraries:

```bash
python -m pip install pandas
python -m pip install matplotlib
```

3. Run the pipeline:

```bash
python main.py
```

4. Monitor the dashboards for live values, running averages, and queue telemetry.

## Requirements

* Python 3.10+
* pandas (`pip install pandas`)
* matplotlib (`pip install matplotlib`)

## Authors

* Sabaina Ijaz
* Nuwaira Batool
