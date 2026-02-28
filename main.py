import json
from core.engine import TranformationEngine
from plugins.inputs import CsvReader, JsonReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter

# Simple Pythonic Factory
INPUT_DRIVERS = {"json": JsonReader, "csv": CsvReader}
OUTPUT_DRIVERS = {"console": ConsoleWriter, "file": GraphicsChartWriter}

def bootstrap():
    # 1. Load config.json
    # 2. Instantiate Output (the Sink)
    # 3. Instantiate Core (inject the Sink)
    # 4. Instantiate Input (inject the Core)
    # 5. Run the Input
