from typing import List, Any
from core.contracts import DataSink

class TranformationEngine:
    def __init__(self, sink: DataSink):
        self.sink = sink

    def execute(self, raw_data: List[Any]) -> None:
        # 1. Transform data
        # 2. Send to the abstraction
        self.sink.write(raw_data)


    def clean_data(self, data):
        # making continent into region
        if "Continent" in data.columns:
            data = data.rename(columns={"Continent": "Region"})
        
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
                "Region": r[0]["Region"],
                "Year": int(r[1]),
                "Value": float(r[0][r[1]])
            },
                filter(
                    lambda r:r[0].get(r[1]) not in ("",None),
                    ((row,year) for row in records for year in year_cols)
                )
            )
        )
        
        #removing invalid gdp values 
        cleaned = list(filter(lambda r: r["Value"] >= 0, data_long))
        
        return cleaned
    
    def filter_data(cleaned_data, config):
        region = config.get("region", [])
        
        if isinstance(region, str):
            regions = list(map(lambda r: r.strip().lower(), filter(None, region.split(","))))
        elif isinstance(region, list):
            regions = list(map(lambda r: r.strip().lower(), region))
        else: 
            regions = []

        country = config.get("country", "").strip().lower()
        year = config.get("year")

        return list(filter(lambda r:
            (not regions or r["Region"].lower() in regions) and
            (not country or r["Country Name"].lower() == country) and
            (not year or r["Year"] == year)
        , cleaned_data))

    def compute_data(self, filtered_data, config):
        if not filtered_data:
            raise ValueError("No data available for computation after filtering.")
        
        #op is the operation we need to perform (sum/avg)
        op = config.get("operation","").lower()
        
        #handling null case
        gdp_values = list(map(lambda r:r["Value"],filtered_data))
        if op == "average":
            return sum(gdp_values)/len(gdp_values) if gdp_values else 0
        elif op == "sum":
            return sum(gdp_values)
        else:
            raise ValueError(f"Unknown operation: {op}")