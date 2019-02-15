def friendly_url(title):
    result = title
    if len(title) > 25:
        result = ''.join([word[0] for word in result.split(' ')])

    replacements = {
        ' ': '-',
        '?': '',
    }
    for before, after in replacements.items():
        result = result.replace(before, after)

    while url_exists(result):
        result = result + '1'

    save_url(result)
    return result


def test_friendly_url():
    assert friendly_url('hello') == 'hello'
    assert friendly_url('hello world') == 'hello-world'
    assert friendly_url('can you hear me?') == 'can-you-hear-me'


def test_friendly_url_long_names():
    assert friendly_url('really long long long long title') == 'rllllt'
    # Discuss ever longer list of bad characters if hard-coding


def test_friendly_url_duplicates():
    '''
    There are two helper functions for this part:
    save_url(url) -> None
    url_exists(url) -> bool
    '''

    assert friendly_url('no dupes') == 'no-dupes'
    assert friendly_url('no dupes') == 'no-dupes1'
    assert friendly_url('no dupes') == 'no-dupes11'

    # Quick solution adds extra character as above. If time deal with nicer
    # enumeration eg
    # no-dupes1, no-dupes2, ...

    # Now discuss how this would work with a real DB rather than in-memory.
    # How do we test a url without writing it to the DB and repeat to
    # demonstrate no dupes still works



###############################################################################
# Code to make task work
###############################################################################

import os
import pytest
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


def main():

    filename = os.path.basename(__file__)
    pytest.main([filename])


if __name__ == '__main__':
    main()
