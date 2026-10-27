import uvicorn
import os
import sys
from pathlib import Path

# Add backend directory to sys.path so 'app' can be imported anywhere
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} on {settings.HOST}:{settings.PORT}")
    print(f"Interactive Swagger documentation available at: http://localhost:{settings.PORT}/docs")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
