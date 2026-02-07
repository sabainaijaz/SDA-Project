import pandas as pd

def clean_data(data):
    # making continent into region
    if "Continent" in data.columns:
        data = data.rename(columns={"Continent": "Region"})
    
    # in the og file every year is a new column
    #turning columns into rows so its easier to filter later on 
    #the GDP under the years goes under the values column accordingly
    year_cols = [col for col in data.columns if col.isdigit()]
    data_long = data.melt(
        id_vars=["Country Name", "Region"],  # columns which willl have no changhe
        value_vars=year_cols,                 # all cols converting to rows of year 1960-2024 all comes under year
        var_name="Year",                      #name for the column header
        value_name="Value"                    # name for the gdp column header
    )
  #deleting rows with missing values
    data_long = data_long.dropna(subset=["Country Name", "Region", "Year", "Value"])
    
    data_long["Year"] = data_long["Year"].astype(int)
    data_long["Value"] = data_long["Value"].astype(float)
    
    data_long = data_long[data_long["Value"] >= 0]

    # converting to list of dict
    cleaned_records = data_long.to_dict(orient="records")
    
    return cleaned_records
