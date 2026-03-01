import json
from core.engine import TranformationEngine
from plugins.inputs import CsvReader, JSONReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter

# Simple Pythonic Factory
INPUT_DRIVERS = {"json": JSONReader, "csv": CsvReader}
OUTPUT_DRIVERS = {"console": ConsoleWriter, "graphics": GraphicsChartWriter}

def bootstrap():
    # 1. Load config.json
    with open("config.json", "r") as f:
        config = json.load(f)

    # 2. Instantiate Output (the Sink)
    if config["output"] not in OUTPUT_DRIVERS:
        raise ValueError(f"Unsupported output type: {config['output']}")
    output_type = config["output"]
    
    if output_type == "graphics":
        chart_type = config.get("chart_type", "line")
        sink = OUTPUT_DRIVERS[output_type](chart_type)
    else:
        sink = OUTPUT_DRIVERS[output_type]()

    # 3. Instantiate Core (inject the Sink)
    engine = TranformationEngine(sink, config)

    # 4. Instantiate Input (inject the Core)
    if config["input"] not in INPUT_DRIVERS:
        raise ValueError(f"Unsupported input type: {config['input']}")
    input_type = config["input"]
    input_driver = INPUT_DRIVERS[input_type](engine)

    # 5. Run the Input
    input_driver.read(config["input_file"])

if __name__ == "__main__":
    bootstrap()