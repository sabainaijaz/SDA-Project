def filter_data(config, cleaned_data):
    return list(filter(lambda r: (config.get("region") is None or r["Region"] == config["region"]) and
                              (config.get("country") is None or r["Country Name"] == config["country"]) and
                              (r["Year"] == config["year"]), cleaned_data))
 

