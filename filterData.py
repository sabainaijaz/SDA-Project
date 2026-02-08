def filter_data(cleaned_data, config):
    region = config.get("region", "").strip().lower()
    country = config.get("country", "").strip().lower()
    year = config.get("year")

    return list(filter(lambda r:
        (not region or r["Region"].lower() == region) and
        (not country or r["Country Name"].lower() == country) and
        (not year or r["Year"] == year)
    , cleaned_data))