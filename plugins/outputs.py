from typing import List
import matplotlib.pyplot as plt 

class ConsoleWriter:
    def write(self, records: List[dict]) -> None:
        for record in records:
            print(f"DEBUG: {record}")

class GraphicsChartWriter: 
