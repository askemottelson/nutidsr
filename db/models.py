from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import TEXT
from sqlalchemy import Column, String, Integer, ForeignKey

Base = declarative_base()


class Word(Base):
    __tablename__ = "word"
    id = Column(Integer, primary_key=True)
    word = Column(String(1000))
    description = Column(TEXT)
    category = Column(String(100))
    forms = relationship("Form")


class Form(Base):
    __tablename__ = "form"
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id'))
    word = relationship("Word", back_populates="forms")
    index = Column(Integer)
    form = Column(String(100))
