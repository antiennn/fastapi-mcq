from fastapi import FastAPI, Depends
from sqladmin import Admin
from sqlalchemy.orm import Session

from config import settings
from database import get_db, engine
from gemini_config.models.gemini_model import Gemini
from internals.admin import AdminAuth
from internals.models.gemini_admin import GeminiAdmin
from internals.models.question_admin import QuestionAdmin

app = FastAPI()
authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)
admin = Admin(app, engine, base_url="/admin",
              authentication_backend=authentication_backend,
              title="Multiple Choice Questions")

admin.add_view(QuestionAdmin)
admin.add_view(GeminiAdmin)

@app.get("/ping")
def read_root():
    return {"message": "pong"}
