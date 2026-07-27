from fastapi import FastAPI

from app.routes.chat_routes import router as chat_router

from app.core.database import engine
from app.models.db_models import Base
from app.routes.upload_routes import (
    router as upload_router
)
from app.models.conversation_summary import ConversationSummary


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(chat_router)
app.include_router(upload_router)

@app.get("/")
def home():
    return {"message": "AI Chatbot Backend Running"}