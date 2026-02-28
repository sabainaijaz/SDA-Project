from typing import List, Any
from core.contracts import DataSink
import math

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
       # data is already a list of dicts
       year_cols = list(filter(lambda c: str(c).isdigit(), data[0].keys()))

       data_long = list(
         map(
            lambda r: {
                "Country Name": r[0]["Country Name"],
                "Continent": r[0]["Continent"],
                "Year": int(r[1]),
                "GDP": float(r[0][r[1]])
            },
            filter
            (
                lambda r: r[0].get(r[1]) not in ("", None) and
                          not (isinstance(r[0].get(r[1]), float) and math.isnan(r[0].get(r[1]))),
                ((row, year) for row in data for year in year_cols)
            )
         )
       )
 
       cleaned = list(filter(lambda r: r["GDP"] >= 0, data_long))
       return cleaned
    
    def filter_data(self,cleaned_data, config):
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
        from collections import defaultdict
        from functools import reduce

        year_range = config.get("year_range", [])
        startYear, endYear = year_range if len(year_range) == 2 else (None, None)
        decline_years = config.get("decline_years", 5)

        # 1. Top 10 GDP
        def compute_top10():
            year_data = list(filter(lambda r: r["Year"] == endYear, filtered_data))
            return list(map(lambda r: {"Country Name": r["Country Name"], "GDP": r["GDP"]},
                    sorted(year_data, key=lambda x: x["GDP"], reverse=True)[:10]))

        # 2. Bottom 10 GDP
        def compute_bottom10():
            year_data = list(filter(lambda r: r["Year"] == endYear, filtered_data))
            return list(map(lambda r: {"Country Name": r["Country Name"], "GDP": r["GDP"]},
                    sorted(year_data, key=lambda x: x["GDP"])[:10]))

        # 3. GDP Growth Rate
        def compute_growth():
            country_dict = reduce(
                lambda acc, r: {**acc, r["Country Name"]: acc.get(r["Country Name"], []) + [r]},
                filtered_data, {}
            )
            return list(filter(None, map(
                lambda item: {
                    "Country Name": item[0],
                    "Start GDP": sorted(item[1], key=lambda x: x["Year"])[0]["GDP"],
                    "End GDP": sorted(item[1], key=lambda x: x["Year"])[-1]["GDP"],
                    "Growth Rate %": (
                        (sorted(item[1], key=lambda x: x["Year"])[-1]["GDP"] -
                         sorted(item[1], key=lambda x: x["Year"])[0]["GDP"]) /
                        sorted(item[1], key=lambda x: x["Year"])[0]["GDP"]
                    ) * 100
                } if sorted(item[1], key=lambda x: x["Year"])[0]["GDP"] != 0 else None,
                country_dict.items()
            )))

        # 4. Average GDP by Continent
        def compute_average():
            continent_dict = reduce(
                lambda acc, r: {**acc, r["Continent"]: acc.get(r["Continent"], []) + [r["GDP"]]},
                filtered_data, {}
            )
            return list(map(
                lambda item: {"Continent": item[0], "Average GDP": sum(item[1]) / len(item[1])},
                continent_dict.items()
            ))

        # 5. Global GDP Trend
        def compute_trend():
            year_dict = reduce(
                lambda acc, r: {**acc, r["Year"]: acc.get(r["Year"], 0) + r["GDP"]},
                filtered_data, {}
            )
            return list(map(
                lambda item: {"Year": item[0], "Total GDP": item[1]},
                sorted(year_dict.items())
            ))

        # 6. Fastest Growing Continent
        def compute_fastest():
            continent_dict = reduce(
                lambda acc, r: {**acc, r["Continent"]: acc.get(r["Continent"], []) + [r]},
                filtered_data, {}
            )
            growth = dict(filter(lambda item: item[1] is not None, map(
                lambda item: (
                    item[0],
                    ((sum(r["GDP"] for r in item[1] if r["Year"] == endYear) -
                      sum(r["GDP"] for r in item[1] if r["Year"] == startYear)) /
                     sum(r["GDP"] for r in item[1] if r["Year"] == startYear)) * 100
                    if sum(r["GDP"] for r in item[1] if r["Year"] == startYear) != 0 else None
                ),
                continent_dict.items()
            )))
            fastest = max(growth, key=growth.get) if growth else None
            return {"Continent": fastest, "Growth Rate %": growth[fastest]} if fastest else {}

        # 7. Consistent GDP Decline
        def compute_decline():
            country_dict = reduce(
                lambda acc, r: {**acc, r["Country Name"]: acc.get(r["Country Name"], []) + [r]},
                filtered_data, {}
            )
            return list(filter(None, map(
                lambda item: {"Country Name": item[0]}
                if len(sorted(item[1], key=lambda x: x["Year"])[-decline_years:]) == decline_years
                and all(
                    earlier > later for earlier, later in zip(
                        list(map(lambda r: r["GDP"], sorted(item[1], key=lambda x: x["Year"])[-decline_years:])),
                        list(map(lambda r: r["GDP"], sorted(item[1], key=lambda x: x["Year"])[-decline_years:]))[1:]
                    )
                ) else None,
                country_dict.items()
            )))

        # 8. Continent GDP Contribution
        def compute_contribution():
            continent_dict = reduce(
                lambda acc, r: {**acc, r["Continent"]: acc.get(r["Continent"], 0) + r["GDP"]},
                filtered_data, {}
            )
            total = sum(continent_dict.values())
            return list(map(
                lambda item: {"Continent": item[0], "Contribution %": (item[1] / total) * 100},
                continent_dict.items()
            )) if total != 0 else []

        
        dispatch = {
            "top10": compute_top10,
            "bottom10": compute_bottom10,
            "growth": compute_growth,
            "average": compute_average,
            "trend": compute_trend,
            "fastest": compute_fastest,
            "decline": compute_decline,
            "contribution": compute_contribution
        }

        return dict(map(
            lambda analysis: (analysis, dispatch[analysis]()),
            filter(lambda a: a in dispatch, config.get("analysis", []))
        ))