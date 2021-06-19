import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table ,DateTime
from sqlalchemy.orm import relationship
from .init_pre import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s')>" % (self.id, self.name, self.phone, self.requisites)

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)

    def __init__(self, id):
        self.id = id

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, file_id):
        self.file_id = file_id

# association_files_seller = Table('offer_file1', Base.metadata,
#     Column('offer_id', Integer, ForeignKey('offer.id')),
#     Column('file_id', Integer, ForeignKey('file.id'))
# )

    # files_seller = relationship("File",
    #                 secondary=association_files_seller)

# __all__ = ['User', 'File']