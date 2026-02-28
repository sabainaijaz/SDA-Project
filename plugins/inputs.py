import json
import re
from core.contracts import PipelineService

# class CsvReader:


class JSONReader:
    def __init__(self, pipeline: PipelineService):
        self.pipeline = pipeline

    def read(self, file_path: str) -> None:
        try:
            with open(file_path, "r") as f:
                data = f.read()

            # replacing NaN with null
            data = data.replace("NaN", "null")

            # replacing corruptes years values
            data = re.sub(r'("?\d{4}"?\s*:\s*)([^,\n}]+)', lambda m: m.group(1) + (m.group(2) if self.__is_valid_number(m.group(2)) else "null"), data)

            data = json.loads(data)
            
            self.pipeline.execute(data)

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in file: {file_path}")
        except Exception as e:
            print(f"Error reading JSON file: {e}")

    def __is_valid_number(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False