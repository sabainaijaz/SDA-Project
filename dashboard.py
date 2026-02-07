import json
import pandas as pd
from loadData import load_data
from cleanData import clean_data
from filterData import filter_data
from computeData import compute_data


with open("config.json") as f:
    config=json.load(f)
data=load_data("GDP-Data.csv")
cleaned=clean_data(data)
filtered=filter_data(cleaned,config)
print("Number of rows after filtering:", len(filtered))
print("Sample rows:", filtered[:5])

computation=compute_data(filtered,config)
print("Computation results:", computation)