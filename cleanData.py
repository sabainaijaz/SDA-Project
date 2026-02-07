import pandas as pd
def clean_data(data):
    #we will check if the data set has all of these columns to be able to proceed witht he cleaning of the code
    required_cols=["Country Name","Region","Year","Value"]
    if not all(col in data.columns for col in required_cols):
        missing=[col for col in required_cols if col not in data.columns]
        raise KeyError(f"Missing required columns:{missing}")
    
    #convertin the data frame into list of dictionaries
    final_records=data.to_dict(orient="records")


    def clean_record(record):
        #removing extra spaces
        record["Country Name"]=record["Country Name"].strip() if record["Country Name"] else ""
        record["Region"]=record["Region"].strip() if record["Region"] else ""

        try:
             record["Year"]=int(record["Year"])
             record["Value"]=float(record["Value"])
        except:
             return None 
         #removing invalid rows
        if record["Value"]<0:
             return None
        if not all(record[col] for col in required_cols):
             return None
        return record

    cleaned=list(filter(lambda r:r is not None,map(clean_record,final_records)))
    
    return cleaned