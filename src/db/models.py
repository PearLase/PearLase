from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)
    place_id = Column(String, unique=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    status = Column(String, default='discovered') # discovered, contacted, onboarding, completed

    # Collected Info
    tax_id = Column(String, nullable=True)
    authorized_person = Column(String, nullable=True)

    last_contact = Column(DateTime, default=datetime.datetime.utcnow)

class MessageLog(Base):
    __tablename__ = 'message_logs'

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer)
    role = Column(String) # assistant or user
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def init_db(db_url="sqlite:///./automation.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

if __name__ == "__main__":
    init_db()
