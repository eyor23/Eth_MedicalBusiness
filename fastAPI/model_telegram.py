from sqlalchemy import Column, Integer, String, BigInteger, Text, TIMESTAMP
from database import Base

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'

    id = Column(Integer, primary_key=True, index=True)
    channel_title = Column(Text)
    channel_username = Column(Text)
    message_id = Column(BigInteger, unique=True, index=True)
    message = Column(Text)
    message_date = Column(TIMESTAMP)
    media_path = Column(Text)
    emoji_used = Column(Text)
    youtube_links = Column(Text)
