import mock
import sys
import pytest

from org.company.frobnicator import Frobnicator


def fake_get(url, headers=None):
    return mock.Mock(json=[{'apples': 4}])

@mock.patch('org.company.frobnicator.requests.get', side_effect=fake_get)
def test_queries(requests_get):
    """Shows how requests.get is mocked in a test"""
    Frobnicator().queries()


if __name__ == "__main__":
    pytest.main(sys.argv)
