from sqlalchemy import MetaData, create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

metadata = MetaData()
engine = create_engine('sqlite:///arcold.db', connect_args={'check_same_thread':False}, echo=False)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()

class Cage(Base):
    __tablename__ = 'cages'
    id = Column(Integer, primary_key=True)
    cage_name = Column(String)

    lick_data = relationship("Lick_event")

class Lick_event(Base):
    __tablename__ = 'licking_events'
    id = Column(Integer, primary_key=True)
    cage_id = Column(ForeignKey('cages.id'))
    starting_time = Column(DateTime)
    final_time = Column(DateTime)

def get_cages():
    return db_session.query(Cage)

data = get_cages()