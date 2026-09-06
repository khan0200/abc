import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Education Center CRM"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./education_crm.db")

settings = Settings()
