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