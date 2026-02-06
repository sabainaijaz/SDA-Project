import pandas as pd

def load_data(file_path): 
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"No data: {file_path} is empty.")
    except Exception as e:
        raise Exception(f"An error occurred while loading data: {e}")
    
