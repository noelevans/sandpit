from functools import lru_cache
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class URL(Base):
    __tablename__ = 'urls'
    link = Column(String(64), primary_key=True)


def save_url(url_path):
    new_url = URL(link=url_path)
    session().add(new_url)
    session().commit()


def url_exists(url_path):
    return bool(session().query(URL).filter(URL.link==url_path).count())


@lru_cache(maxsize=None)
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
