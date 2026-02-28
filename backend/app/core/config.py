import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    PROJECT_NAME: str = "SupportLens API"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data.db"
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    HF_MODEL_ID: str = os.getenv(
        "HF_MODEL_ID", "meta-llama/Llama-3.2-3B-Instruct")


settings = Settings()
