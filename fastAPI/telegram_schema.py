from pydantic import BaseModel
from datetime import datetime

class TelegramMessageBase(BaseModel):
    channel_title: str
    channel_username: str
    message_id: int
    message: str
    message_date: datetime
    media_path: str
    emoji_used: str
    youtube_links: str

class TelegramMessageCreate(TelegramMessageBase):
    pass

class TelegramMessageUpdate(TelegramMessageBase):
    pass

class TelegramMessage(TelegramMessageBase):
    id: int

    class Config:
        orm_mode = True
