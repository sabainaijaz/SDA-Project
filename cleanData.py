import pandas as pd

def clean_data(data):
    # making continent into region
    if "Continent" in data.columns:
        data = data.rename(columns={"Continent": "Region"})
    
    # in the og file every year is a new column
    #turning columns into rows so its easier to filter later on 
    #the GDP under the years goes under the values column accordingly
    year_cols = list(filter(lambda c: c.isdigit(), data.columns))

   

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
                ((row,year) for row in data.to_dict(orient="records")
                            for year in filter(str.isdigit, data.columns))
            )
        )
    )
    
    #removing invalid gdp values 
    cleaned = list(filter(lambda r: r["Value"] >= 0, data_long))
    
    return cleaned
