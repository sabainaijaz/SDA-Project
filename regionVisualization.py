import matplotlib.pyplot as plt

def region_visualization(filtered_data, limit=10):
    if not filtered_data:
        raise ValueError("No data available for visualization after filtering.")
        
    country_values = {}
    list(map(lambda r: country_values.setdefault(r["Country Name"], []).append(r["Value"]), filtered_data))

    # choosing the first gdps
    country_gdp = dict(map(lambda kv: (kv[0], kv[1][0]), country_values.items()))
    country_gdp = dict(filter(lambda kv: kv[1] >= 0, country_gdp.items()))

    # sorting
    sorted_gdp = sorted(country_gdp.items(), key=lambda kv: kv[1], reverse=True)

    # picking the counties based of the limit
    #the other countries will be grouped into other
    top_countries = sorted_gdp[:limit]
    other_gdp = sum(map(lambda kv: kv[1], sorted_gdp[limit:]))
    if other_gdp > 0:
        top_countries.append(("Other", other_gdp))

    
    countries, values = list(map(lambda kv: kv[0], top_countries)), list(map(lambda kv: kv[1], top_countries))

   
    colors = plt.cm.tab20.colors  
    pie_colors = colors[:len(countries)]
    bar_colors = colors[:len(countries)]

    #pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=countries, autopct="%1.1f%%", startangle=140, colors=pie_colors)
    plt.title("Region(s) GDP Distribution (Pie chart)")
    plt.axis("equal")
    plt.show()

    #bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(countries[::-1], values[::-1], color=bar_colors[::-1])
    plt.xlabel("GDP Value")
    plt.ylabel("Country")
    plt.title("Region(s) GDP Distribution (Bar chart)")
    plt.tight_layout()
    plt.show()
