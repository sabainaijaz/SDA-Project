def filter_data(cleaned_data, config):
    region = config.get("region", "").strip().lower()
    country = config.get("country", "").strip().lower()
    year = config.get("year")

    def match_row(r):
        new_region = r["Region"].strip().lower()
        new_country = r["Country Name"].strip().lower()
        #to match the country/region in config with the one in each row
        return (
            (not region or new_region == region) and
            (not country or new_country == country) and
            r["Year"] == year
        )

    
    filtered = list(filter(match_row, cleaned_data))
    return filtered
