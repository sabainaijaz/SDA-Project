def validate_config(config):
    #making sure that all the required keys are present in the config file
    required_keys = ["year", "operation", "region", "country"]

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # year should be an integer 
    if not isinstance(config["year"], int):
        raise ValueError("Year must be an integer.")
    
    # operation should be sum or avg, nothing else
    if config["operation"].lower() not in ("sum", "average"):
        raise ValueError("Operation must be either 'sum' or 'average'.")
    
    # either region should be present or country should be present. 
    if not config.get("region") and not config.get("country"):
        raise ValueError("At least one of 'region' or 'country' must be specified")