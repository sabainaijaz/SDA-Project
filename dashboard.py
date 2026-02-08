import json
import pandas as pd
from loadData import load_data
from cleanData import clean_data
from filterData import filter_data
from computeData import compute_data
from validateConfig import validate_config
from countryVisualization import country_visualization
from regionVisualization import region_visualization
def show_error(msg):
    print(f"Error: {msg}")
try:
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
except FileNotFoundError as e:
    show_error(str(e))
except ValueError as e:
    show_error(str(e))
except KeyError as e:
    show_error(f"Missing required configuration field: {e}")
except Exception as e:
    show_error(f"Unexpected error occurred: {e}")
#exception handling for visualization 
try:
    if config.get("country"):
        country_visualization(cleaned, config)

    else:
        region_visualization(filtered, limit=5)
except ValueError as ve:
    print(f"Visualization Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred during visualization: {e}")