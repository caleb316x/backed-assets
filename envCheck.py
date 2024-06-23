import os
from dotenv import load_dotenv, find_dotenv

def load_and_validate_env(env_path='.env'):
    required_vars = ['chain','collections','start_page','max_page','asset_per_page','order']
    env_file = find_dotenv(env_path)
    
    if not env_file:
        print(f".env file not found at path: {env_path}")
        return False

    load_dotenv(env_file)

    if required_vars:
        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        else:
            print("All required environment variables are present.")
    
    return { 
            'chain': os.getenv("chain"),
            'collections': os.getenv("collections"),
            'start_page':  int(os.getenv("start_page")),
            'max_page': int(os.getenv("max_page")),
            'asset_per_page':  int(os.getenv("asset_per_page")),
            'order': os.getenv("order")
            }
