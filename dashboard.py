import json
import pandas as pd
from loadData import load_data
from cleanData import clean_data
from filterData import filter_data
from computeData import compute_data
from validateConfig import validate_config
from countryVisualization import country_visualization

with open("config.json") as f:
    config=json.load(f)

data = load_data("GDP-Data.csv")

cleaned = clean_data(data)
validate_config(config, cleaned)
filtered = filter_data(cleaned,config)
result = compute_data(filtered,config)

print("Configuration:")

#need to print the config line by line 
list(map(lambda kv: print(f"{kv[0]}: {kv[1]}"), config.items()))

print("\nComputation results:", result)

if config.get("country"):
    country_visualization(cleaned, config)

