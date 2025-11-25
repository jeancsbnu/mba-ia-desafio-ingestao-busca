import os
from dotenv import load_dotenv

load_dotenv()


def get_required_env_vars(required_vars=None):
    if required_vars is None:
        required_vars = (
            "GOOGLE_API_KEY",
            "GOOGLE_EMBEDDING_MODEL",
            "DATABASE_URL",
            "PG_VECTOR_COLLECTION_NAME",
            "PDF_PATH",
            "GOOGLE_MODEL"
        )
    
    # Check all required variables
    for var_name in required_vars:
        if os.getenv(var_name) is None:
            raise ValueError(f"Environment variable {var_name} is not set.")
    
    # Return all variables as a dictionary
    return {var_name: os.getenv(var_name) for var_name in required_vars}

