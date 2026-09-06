from sqlalchemy import Column, Integer, String, Float, Boolean
from backend.app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    level = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="$")
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "price": self.price,
            "currency": self.currency,
            "description": self.description,
            "is_active": self.is_active
        }
