import enum
from datetime import datetime
from app import db 

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Enum, Boolean

class PostCategory(enum.Enum):
    news = 'Новина'
    publication = 'Публікація'
    tech = 'Технології'
    other = 'Інше'

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(Enum(PostCategory), default=PostCategory.other)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    author: Mapped[str] = mapped_column(String(20), default='Anonymous')

    def __repr__(self):
        return f'<Post(title={self.title})>'