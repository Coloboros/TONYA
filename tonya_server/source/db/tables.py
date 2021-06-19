import datetime
from sqlalchemy import Sequence, Column, Integer, String, ForeignKey, Table ,DateTime
from sqlalchemy.orm import relationship
from .init_pre import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)
    child_bots = relationship("Bot")

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s')>" % (self.id, self.name, self.phone, self.requisites)

class Bot(Base):
    __tablename__ = 'bot'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    parent = relationship("User", back_populates="child_bots")

class Tocken(Base):
    __tablename__ = 'auth_tocken'
    id = Column('id', Integer, Sequence('some_id_seq'), primary_key=True)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    parent = relationship("User")

    def __init__(self, value):
        self.value = value

# association_files_seller = Table('offer_file1', Base.metadata,
#     Column('offer_id', Integer, ForeignKey('offer.id')),
#     Column('file_id', Integer, ForeignKey('file.id'))
# )

    # files_seller = relationship("File",
    #                 secondary=association_files_seller)

# __all__ = ['User', 'File']