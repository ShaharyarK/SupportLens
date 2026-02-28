from huggingface_hub import InferenceClient
from app.core.config import settings

client = InferenceClient(model=settings.HF_MODEL_ID, token=settings.HF_TOKEN)
