from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from typing import TYPE_CHECKING
from datetime import datetime, timezone 

if TYPE_CHECKING:
    from app.posts.models import Post

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): 
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.png')
    
    about_me: Mapped[str | None] = mapped_column(String(140))
    
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<User {self.username}>'