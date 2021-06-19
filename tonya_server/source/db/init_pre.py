from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..settings import TELEGRAM_BOT_TOKEN


engine = create_engine(TELEGRAM_BOT_TOKEN, echo=False)

Base = declarative_base()

__all__ = ['Base', 'engine']
