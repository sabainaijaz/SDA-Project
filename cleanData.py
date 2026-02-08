import pandas as pd

def clean_data(data):
    # making continent into region
    if "Continent" in data.columns:
        data = data.rename(columns={"Continent": "Region"})
    
    # in the og file every year is a new column
    #turning columns into rows so its easier to filter later on 
    #the GDP under the years goes under the values column accordingly
    year_cols = list(filter(lambda c: c.isdigit(), data.columns))

    records = data.to_dict(orient="records") 

    #convdrting wide to long format
    data_long = [
        {
            "Country Name": row["Country Name"],
            "Region": row["Region"],
            "Year": int(year),
            "Value": float(row[year])
        }
        for row in records
        for year in year_cols
        if row.get(year) not in ("", None)
    ]
    
    #removing invalid gdp values 
    cleaned = list(filter(lambda r: r["Value"] >= 0, data_long))
    
    return cleaned
