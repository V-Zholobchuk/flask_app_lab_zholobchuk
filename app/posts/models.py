import enum
from datetime import datetime
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, Enum, Boolean, ForeignKey, Integer, Table, Column

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.users.models import User


post_tags = db.Table('post_tags',
    db.Model.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class PostCategory(enum.Enum):
    news = 'Новина'
    publication = 'Публікація'
    tech = 'Технології'
    other = 'Інше'

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(Enum(PostCategory), default=PostCategory.other)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags, 
        back_populates="posts"
    )
    # ---

    def __repr__(self):
        return f'<Post(title={self.title})>'

class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags, 
        back_populates="tags"
    )

    def __repr__(self):
        return f'<Tag {self.name}>'