from pydantic import BaseModel
from typing import Literal


class TranslateRequest(BaseModel):
    source_text: str
    source_language: str
    target_language: str


class TranslateResponse(BaseModel):
    target_text: str


class FeedbackRequest(BaseModel):
    translation_id: str
    feedback: Literal['thumbs_up', 'thumbs_down']
