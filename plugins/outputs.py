import matplotlib.pyplot as plt

class ConsoleWriter:
    def write(self, records):
        list(map(self._dispatch, records.items()))

    def _dispatch(self, item):
        analysis, data = item
        print(analysis)
        print(data)

class GraphicsChartWriter:
    def __init__(self, chart_type: str):
        self.chart_type = chart_type

    def write(self, records: dict) -> None:
        list(map(self._dispatch, records.items()))

    def _dispatch(self, item):
        analysis, data = item

        if self.chart_type == "line":
            self._write_line_chart(analysis, data)
        elif self.chart_type == "bar":
            self._write_bar_chart(analysis, data)
        elif self.chart_type == "scatter":
            self._write_scatter_chart(analysis, data)
        elif self.chart_type == "pie":
            self._write_pie_chart(analysis, data)
        else:
            print(f"Unsupported chart type: {self.chart_type}")

    def _write_line_chart(self, analysis: str, data: list) -> None:
        if analysis == "trend":
            x = list(map(lambda r: r["Year"], data))
            y = list(map(lambda r: r["Total GDP"], data))
            plt.figure()
            plt.plot(x, y, marker='o')
            plt.title("Global GDP Trend")
            plt.xlabel("Year")
            plt.ylabel("Total GDP")
            plt.tight_layout()
            plt.show()

        else:
            print(f"Line chart not supported for: {analysis}")

    def _write_bar_chart(self, analysis: str, data: list) -> None:
        if analysis in ("top10", "bottom10"):
            x = list(map(lambda r: r["Country Name"], data))
            y = list(map(lambda r: r["GDP"], data))
            plt.figure()
            plt.bar(x, y)
            plt.title(f"{analysis.upper()} Countries by GDP")
            plt.xlabel("Country")
            plt.ylabel("GDP")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        elif analysis == "average":
            x = list(map(lambda r: r["Continent"], data))
            y = list(map(lambda r: r["Average GDP"], data))
            plt.figure()
            plt.bar(x, y)
            plt.title("Average GDP by Continent")
            plt.xlabel("Continent")
            plt.ylabel("Average GDP")
            plt.tight_layout()
            plt.show()

        elif analysis == "growth":
            data_sorted = sorted(data, key=lambda r: r["Growth Rate %"], reverse=True)

            top = 15
            data_limit = data_sorted[:top]
            
            countries = list(map(lambda r: r["Country Name"], data_limit))
            growth = list(map(lambda r: r["Growth Rate %"], data_limit))

            plt.figure(figsize=(10, 6))
            plt.barh(countries, growth)
            plt.title(f"Top {top} GDP Growth Rate by Country")
            plt.xlabel("Growth Rate %")
            plt.ylabel("Country")
            plt.tight_layout()
            plt.show()

        else:
            print(f"Bar chart not supported for: {analysis}")

    def _write_scatter_chart(self, analysis: str, data: list) -> None:
        if analysis == "trend":
            x = list(map(lambda r: r["Year"], data))
            y = list(map(lambda r: r["Total GDP"], data))
            plt.figure()
            plt.scatter(x, y)
            plt.title("Global GDP Trend")
            plt.xlabel("Year")
            plt.ylabel("Total GDP")
            plt.tight_layout()
            plt.show()

        elif analysis in ("top10", "bottom10"):
            x = list(map(lambda r: r["Country Name"], data))
            y = list(map(lambda r: r["GDP"], data))
            plt.figure()
            plt.scatter(x, y)
            plt.title(f"{analysis.upper()} Countries by GDP")
            plt.xlabel("Country")
            plt.ylabel("GDP")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        else:
            print(f"Scatter chart not supported for: {analysis}")

    def _write_pie_chart(self, analysis: str, data: list) -> None:
        if analysis == "contribution":
            labels = list(map(lambda r: r["Continent"], data))
            values = list(map(lambda r: r["Contribution %"], data))
            plt.figure()
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title("Continent GDP Contribution")
            plt.tight_layout()
            plt.show()

        elif analysis == "average":
            labels = list(map(lambda r: r["Continent"], data))
            values = list(map(lambda r: r["Average GDP"], data))
            plt.figure()
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title("Average GDP by Continent")
            plt.tight_layout()
            plt.show()

        elif analysis in ("top10", "bottom10"):
            labels = list(map(lambda r: r["Country Name"], data))
            values = list(map(lambda r: r["GDP"], data))
            plt.figure()
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title(f"{analysis.upper()} Countries by GDP")
            plt.tight_layout()
            plt.show()

        else:
            print(f"Pie chart not supported for: {analysis}")