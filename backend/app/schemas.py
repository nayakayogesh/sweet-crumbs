from datetime import datetime
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Admin(Base):
    __tablename__ = "elden_lord"

    id: Mapped[int] = 1
    user_name: Mapped[str] = mapped_column(String(25))
    