import itertools
import os
import pytest
import re
import string

from db_utils import save_url, url_exists


def friendly_url(title):
    short = title
    if len(title) > 25:
        short = ''.join([word[0] for word in short.split(' ')])

    pre_subs = short.replace(' ', '-')
    result = ''
    for c in pre_subs:
        if c in string.ascii_letters + string.digits + '-':
            result = result + c

    n = itertools.count(1)
    url_no_increment = result
    while url_exists(result):
        without_numbers = re.search('([^0-9]+)', title).groups()
        result = url_no_increment + str(n.__next__())

    save_url(result)
    return result


def test_friendly_url_identity():
    assert friendly_url('hello') == 'hello'


def test_friendly_url_substitution():
    assert friendly_url('hello world') == 'hello-world'
    assert friendly_url('can you hear me?') == 'can-you-hear-me'


def test_friendly_url_long_names():
    assert friendly_url('really long long long long title') == 'rllllt'
    # Discuss ever longer list of bad characters if hard-coding

    # As time goes on we see an ever increasing list of punctuation etc to
    # omit. How can we more easily exclude non alpha-numeric chars?


def test_friendly_url_duplicates():
    '''
    There are two helper functions for this part:
    save_url(url) -> None (Writing to DB)
    url_exists(url) -> bool
    '''

    assert friendly_url('no dupes') == 'no-dupes'
    assert friendly_url('no dupes') == 'no-dupes1'
    assert friendly_url('no dupes') == 'no-dupes2'

    # Quick solution adds extra character as above. If time deal with nicer
    # enumeration eg
    # no-dupes1, no-dupes2, ...

    # Now discuss how this would work with a real DB rather than in-memory.
    # How do we test a url without writing it to the DB and repeat to
    # demonstrate no dupes still works


def main():
    filename = os.path.basename(__file__)
    pytest.main([filename])


if __name__ == '__main__':
    main()
