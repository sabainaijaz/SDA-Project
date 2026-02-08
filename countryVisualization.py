import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def country_visualization(cleaned_data, config):
    country = config.get("country", "").strip().lower()

    if not country:
        raise ValueError("Country must be specified for visualization.")
    
    # filtering data for that country - for all years
    country_data = list(filter(lambda r: r["Country Name"].strip().lower() == country, cleaned_data))

    if not country_data:
        raise ValueError(f"No data available for country: {country}")
    
    # sort the data by year 

    country_data = sorted(country_data, key=lambda r: r["Year"])
    years = list(map(lambda r: r["Year"], country_data))
    values = list(map(lambda r: r["Value"], country_data))

    # line chart: 

    plt.figure()
    plt.plot(years, values)
    plt.title(f"GDP of {country.title()} over the years")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.grid(True)
    plt.show()

    # histogram:

    plt.figure()
    plt.hist(values, bins=20)
    plt.title(f"GDP Distribution of {country.title()}")
    plt.xlabel("GDP")
    plt.ylabel("Frequency")
    plt.show()
