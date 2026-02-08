def compute_data(filtered_data,config):

    if not filtered_data:
        raise ValueError("No data available for computation after filtering.")
    
    #op is the operation we need to perform (sum/avg)
    op = config.get("operation","").lower()
    
    #handling null case
    gdp_values = list(map(lambda r:r["Value"],filtered_data))
    if op == "average":
        return sum(gdp_values)/len(gdp_values) if gdp_values else 0
    elif op == "sum":
        return sum(gdp_values)
    else:
        raise ValueError(f"Unknown operation: {op}")