import os 

def get_base_url():
    return os.getenv("BASE_URL", "http://localhost:8000")