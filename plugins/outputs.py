from typing import List
import matplotlib.pyplot as plt 

class ConsoleWriter:
    def write(self, records: List[dict]) -> None:
        for record in records:
            print(f"DEBUG: {record}")

class GraphicsChartWriter: 
    def __init__(self, chart_type: str):
        self.chart_type = chart_type

    def write(self, records: List[dict]) -> None:
        if self.chart_type == "line":
            self._write_line_chart(records)
        elif self.chart_type == "bar":
            self._write_bar_chart(records)
        elif self.chart_type == "scatter":
            self._write_scatter_chart(records)
        elif self.chart_type == "pie":
            self._write_pie_chart(records)
        else:
            print(f"Unsupported chart type: {self.chart_type}")

    def _write_line_chart(self, records: List[dict]) -> None:
        country = [record["Country"] for record in records]
        gdp = [record["GDP"] for record in records]
        plt.plot(country, gdp)
        plt.title("Line Chart")
        plt.xlabel("Country")
        plt.ylabel("GDP")
        plt.show()

    def _write_bar_chart(self, records: List[dict]) -> None:
        years = [record["Year"] for record in records]
        gdp = [record["GDP"] for record in records]
        plt.bar(years, gdp)
        plt.title("Bar Chart")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()

    def _write_scatter_chart(self, records: List[dict]) -> None:
        years = [record["Year"] for record in records]
        values = [record["GDP"] for record in records]
        plt.scatter(years, values)
        plt.title("Scatter Chart")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()

    def _write_pie_chart(self, records: List[dict]) -> None:
        labels = [record["Country"] for record in records]
        values = [record["Average GDP"] for record in records]
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Pie Chart")
        plt.show()

        

