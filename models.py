from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String(55))
    
    # if you come back later and change something in repr part, this part doesn't require migration because it is not related to our DB
    def __repr__(self):
        return f"\n<User" \
            + f"id={self.id}, " \
            + f"username={self.username}, " \
            + f"email={self.email}, " \
            + ">"