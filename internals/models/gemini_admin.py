from sqladmin import ModelView

from gemini_config.models.gemini_model import Gemini


class GeminiAdmin(ModelView, model=Gemini):
    name = "Gemini keys"
    page_size_options = [25, 50, 100, 200]
    category = "Gemini config"

    can_create = True
    can_delete = True

    column_list = [
        Gemini.id,
        Gemini.access_token,
        Gemini.description,
        Gemini.last_expired_at,
        Gemini
    ]
