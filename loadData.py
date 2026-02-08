import pandas as pd

def load_data(file_path): 
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"No data: {file_path} is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading data: {e}")
    
