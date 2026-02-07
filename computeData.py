
def compute_data(filtered_data,config):
    #op is the operation we need to perform (sum/avg)
    op=config.get("operation","").lower()
    #handling null case
    gdp_values=list(map(lambda r:r["Value"],filtered_data))
    if op=="average":
        answer=sum(gdp_values)/len(gdp_values) if gdp_values else 0
    elif op=="sum":
        answer=sum(gdp_values)
    else:
        raise ValueError(f"Unknown operation: {op}")
    return answer