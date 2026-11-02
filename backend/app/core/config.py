import os
from pathlib import Path
from typing import List

# Find project root (where 'Future Weather Attributes' exists)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent if (BACKEND_DIR.parent / "Future Weather Attributes").exists() else BACKEND_DIR

# Default to the consolidated forecast dataset. Relative overrides are resolved
# from the repository root rather than the process working directory.
DEFAULT_DATASET_REL_PATH = Path("Future Weather Attributes") / "Forecast" / "Final" / "future_daily_weather_attributes.csv"
_dataset_override = os.getenv("WEATHER_DATASET_PATH")
DATASET_PATH = (
    (Path(_dataset_override) if Path(_dataset_override).is_absolute() else PROJECT_ROOT / _dataset_override).resolve()
    if _dataset_override
    else (PROJECT_ROOT / DEFAULT_DATASET_REL_PATH).resolve()
)

class Settings:
    PROJECT_NAME: str = "Japan Disaster & Weather Intelligence API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Dataset configuration
    PROJECT_ROOT_DIR: Path = PROJECT_ROOT
    WEATHER_DATASET_PATH: Path = DATASET_PATH
    
    # CORS Configuration - Allow React Frontend development servers
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "*"  # Allows connection from any dev client
    ]
    
    # Host and port
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
