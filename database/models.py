from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True)
    skills = Column(String)
    ats_score = Column(Integer, default=0)
    resume_text = Column(Text, default="")