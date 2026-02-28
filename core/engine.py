from typing import List, Any
from core.contracts import DataSink

class TranformationEngine:
    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def execute(self, raw_data: List[Any]) -> None:
        # 1. Transform data
        cleaned = self.clean_data(raw_data)
        filtered = self.filter_data(cleaned, self.config)
        result = self.compute_data(filtered, self.config)

        # 2. Send to the abstraction
        self.sink.write(result)


    def clean_data(self, data):
        # making continent into region
        if "Continent" in data.columns:
            data = data.rename(columns={"Continent": "Continent"})
        
        # in the og file every year is a new column
        #turning columns into rows so its easier to filter later on 
        #the GDP under the years goes under the values column accordingly
        year_cols = list(filter(lambda c: c.isdigit(), data.columns))
        records = data.to_dict(orient="records")

        #convdrting wide to long format
        data_long = list(
            map(
                lambda r:{
                "Country Name": r[0]["Country Name"],
                "Continent": r[0]["Continent"],
                "Year": int(r[1]),
                "GDP": float(r[0][r[1]])
            },
                filter(
                    lambda r:r[0].get(r[1]) not in ("",None),
                    ((row,year) for row in records for year in year_cols)
                )
            )
        )
        
        #removing invalid gdp values 
        cleaned = list(filter(lambda r: r["GDP"] >= 0, data_long))
        
        return cleaned
    
    def filter_data(cleaned_data, config):
        continent = config.get("continent", [])
        
        if isinstance(continent, str):
            continents = list(map(lambda r: r.strip().lower(), filter(None, continent.split(","))))
        elif isinstance(continent, list):
            continents = list(map(lambda r: r.strip().lower(), continent))
        else: 
            continents = []

        country = config.get("country", "").strip().lower()
        year_range = config.get("year_range", [])
        if len(year_range) == 2:
           start_year, end_year = year_range
        else:
           start_year = end_year = None


        return list(filter(lambda r:
            (not continent or r["Continent"].lower() in continents) and
            (not country or r["Country Name"].lower() == country) and
            (not start_year or not end_year or start_year <= r["Year"] <= end_year)
            , cleaned_data))
    
    def compute_data(self, filtered_data, config):

        results = {}

        analysis_list = config.get("analysis", [])
        year_range = config.get("year_range", [])

        if len(year_range) == 2:
            startYear, endYear = year_range
        else:
            startYear = endYear = None

        for analysis in analysis_list:
            analysis = analysis.lower()

        #Top 10 GDP (for endYear)
            if analysis == "top10":
                year_data = [r for r in filtered_data if r["Year"] == endYear]
                results["top10"] = sorted(
                year_data, key=lambda x: x["GDP"], reverse=True
            )[:10]

        #Bottom 10 GDP
            elif analysis == "bottom10":
                year_data = [r for r in filtered_data if r["Year"] == endYear]
                results["bottom10"] = sorted(
                year_data, key=lambda x: x["GDP"]
            )[:10]

        #GDP Growth Rate (single country)
            elif analysis == "growth":
                 records_sorted = sorted(filtered_data, key=lambda x: x["Year"])
                 if records_sorted:
                    startGDP = records_sorted[0]["GDP"]
                    endGDP = records_sorted[-1]["GDP"]

                    if startGDP != 0:
                        results["growth"] = (
                        (endGDP - startGDP) / startGDP
                    ) * 100

        #Average GDP
            elif analysis == "average":
                 values = [r["GDP"] for r in filtered_data]
                 results["average"] = sum(values) / len(values) if values else 0

        #Global GDP Trend
            elif analysis == "trend":
               from collections import defaultdict
               year_dict = defaultdict(float)

               for r in filtered_data:
                    year_dict[r["Year"]] += r["GDP"]

               results["trend"] = dict(sorted(year_dict.items()))

        #Fastest Growing Continent
            elif analysis == "fastest":
                from collections import defaultdict
                continent_dict = defaultdict(list)

                for r in filtered_data:
                  continent_dict[r["Continent"]].append(r)

                growth = {}

                for continent, records in continent_dict.items():
                    startGDP = sum(
                    r["GDP"] for r in records if r["Year"] == startYear
                )
                    endGDP = sum(
                    r["GDP"] for r in records if r["Year"] == endYear
                )

                    if startGDP != 0:
                     growth[continent] = (
                        (endGDP - startGDP) / startGDP
                    ) * 100

                if growth:
                    fastest = max(growth, key=growth.get)
                    results["fastest"] = {
                         "continent": fastest,
                         "growth_percent": growth[fastest]
                }

        #Consistent GDP Decline (last 5 years)
            elif analysis == "decline":
                from collections import defaultdict
                country_dict = defaultdict(list)

                for r in filtered_data:
                    country_dict[r["Country Name"]].append(r)

                declining = []

                for country, records in country_dict.items():
                    records_sorted = sorted(records, key=lambda x: x["Year"])[-5:]
                    values = [r["GDP"] for r in records_sorted]

                    if len(values) == 5 and all(
                        earlier > later for earlier, later in zip(values, values[1:])
                ):
                        declining.append(country)

                results["decline"] = declining

        #Continent Contribution
            elif analysis == "contribution":
                 from collections import defaultdict
                 continent_sum = defaultdict(float)
                 total = 0

                 for r in filtered_data:
                  continent_sum[r["Continent"]] += r["GDP"]
                 total += r["GDP"]

                 if total != 0:
                   results["contribution"] = {
                     continent: (val / total) * 100
                     for continent, val in continent_sum.items()
                }
                 else:
                    results["contribution"] = {}

            else:
                 raise ValueError(f"Unknown analysis type: {analysis}")

        return results