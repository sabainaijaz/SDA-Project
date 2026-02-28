
from collections import defaultdict 
#1
def top_10_gdp(engine,data,continent,year):
  filtered=engine.filter_data(data,{"region":continent,"year":year})
  top10=sorted(filtered,key=lambda x: x["GDP"],reverse=True)[:10]
  return [{"Country Name": r["Country Name"], "GDP": r["Value"]} for r in top10]

#2
def bottom_10_gdp(engine,data,continent,year):
  filtered=engine.filter_data(data,{"region":continent,"year":year})
  bottom10=sorted(filtered,key=lambda x: x["GDP"])[:10]
  return [{"Country Name": r["Country Name"], "GDP": r["Value"]} for r in bottom10]

#3
def gdp_growth_rate(engine,data,country,startYear,endYear):
 filtered=[r for r in data if r["Country Name"].lower()==country.lower() and startYear<=r["Year"] <=endYear]
 country_dict=defaultdict(list)
 for r in filtered:
     country_dict[r["Country Name"]].append(r)
 growth={}
 for country, records in country_dict.items():
    records_sorted=sorted(records, key=lambda x: x["Year"])
    start_gdp=records_sorted[0]["GDP"]
    end_gdp=records_sorted[-1]["GDP"]
    if start_gdp !=0:
        growth[country]=((end_gdp-start_gdp)/start_gdp)*100
 return growth

#4
def average_gdp_by_continent(engine,data,startYear,endYear):
    filtered=[r for r in data if startYear<=r["Year"] <=endYear]
    continent_dict=defaultdict(list)
    for r in filtered:
        continent_dict[r["Continent"]].append(r["GDP"])
    return {continent: sum(values)/len(values) for continent, values in continent_dict.items() if values}

#5
def global_gdp_trend(engine, data, startYear, endYear):
    filtered = [r for r in data if startYear <= r["Year"] <= endYear]
    year_dict = defaultdict(float)
    for r in filtered:
        year_dict[r["Year"]] += r["GDP"]
    return dict(sorted(year_dict.items()))

#6
def fastest_growing_continent(engine, data, startYear, endYear):
    filtered = [r for r in data if startYear <= r["Year"] <= endYear]
    continent_dict = defaultdict(list)
    for r in filtered:
        continent_dict[r["Continent"]].append(r)
    growth = {}
    for continent, records in continent_dict.items():
        records_sorted = sorted(records, key=lambda x: x["Year"])
        start_gdp = sum(r["GDP"] for r in records_sorted if r["Year"] == startYear)
        end_gdp = sum(r["GDP"] for r in records_sorted if r["Year"] == endYear)
        if start_gdp != 0:
            growth[continent] = ((end_gdp - start_gdp) / start_gdp) * 100
    fastest = max(growth, key=growth.get)
    return fastest, growth[fastest]

#7
def cosistent_gdp(engine,data,continent,years):
    filtered=[r for r in data if r["Continent"].lower()==continent.lower()]
    country_dict=defaultdict(list)
    for r in filtered:
        country_dict[r["Country Name"]].append(r)
    declining=[]
    for country,records in country_dict.items():
        records_sorted=sorted(records,key=lambda x: x["Year"])[-years:]
        values=[r["GDP"] for r in records_sorted]
        if all(earlier>later for earlier,later in zip(values,values[1:])):
            declining.append(country)
    return declining

#8
def continent_gdp_contribution(engine, data, startYear, endYear):
    filtered = [r for r in data if startYear <= r["Year"] <= endYear]
    continent_sum = defaultdict(float)
    total = 0
    for r in filtered:
        continent_sum[r["Continent"]] += r["GDP"]
        total += r["GDP"]
    return {continent: (val/total)*100 for continent, val in continent_sum.items()}
