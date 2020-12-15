from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Create a URL database then writing and reading records
"""

Base = declarative_base()


class URL(Base):
    __tablename__ = 'urls'
    link = Column(String(64), primary_key=True)


def add_url(session, url):
    new_url = URL(link=url)
    session.add(new_url)
    session.commit()


def main():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    add_url(session, 'hello-world')

    for instance in session.query(URL):
        print(instance, instance.link)

    print(session.query(URL).filter(URL.link=='hello').count())
    print(session.query(URL).filter(URL.link=='hello-world').count())


if __name__ == '__main__':
    main()
