import datetime
from sqlalchemy import Sequence, Column, Float, Integer, String, ForeignKey, Table ,DateTime
from sqlalchemy.orm import relationship
from .init_pre import Base

class User(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)

    tonometr = Column(String)

    birthday = Column(DateTime)
    height = Column(Integer)
    weight = Column(Float)

    child_bots = relationship("Bot")
    tonometr_reports = relationship("TonometrReport")

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.id, self.name, self.phone)

class Bot(Base):
    __tablename__ = 'bot'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    user_id = Column(Integer, ForeignKey('patient.id'))
    parent = relationship("User", back_populates="child_bots")

class Tocken(Base):
    __tablename__ = 'auth_tocken'
    id = Column('id', Integer, Sequence('some_id_seq'), primary_key=True)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(String)
    user_id = Column(Integer, ForeignKey('patient.id'))
    parent = relationship("User")

    def __init__(self, value):
        self.value = value

class TonometrReport(Base):
    __tablename__ = 'tonometr_report'
    id = Column('id', Integer, Sequence('tonometr_report_seq'), primary_key=True)

    top_pressue = Column(Integer)
    bot_pressue = Column(Integer)
    pulse = Column(Integer)

    tags = Column(String)

    user_id = Column(Integer, ForeignKey('patient.id'))
    parent = relationship("User")

    def __init__(self, user_id, top_pressue, bot_pressue, pulse, tags):
        self.user_id = user_id
        self.top_pressue = top_pressue
        self.bot_pressue = bot_pressue
        self.pulse = pulse
        self.tags = tags
# association_files_seller = Table('offer_file1', Base.metadata,
#     Column('offer_id', Integer, ForeignKey('offer.id')),
#     Column('file_id', Integer, ForeignKey('file.id'))
# )

    # files_seller = relationship("File",
    #                 secondary=association_files_seller)

# __all__ = ['User', 'File']