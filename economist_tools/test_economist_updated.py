import os
import pytest
from unittest import mock

import economist_updated


@mock.patch('emailing.send')
def test_alert(mock_send):
    mock_send.return_value = mock.Mock('New Economist', 'test')
    assert 7 == economist_updated.alert('banana')


# @mock.patch('requests')
# @mock.patch('datetime.datetime')
# @mock.patch('time.sleep')
# @mock.patch('emailing.send')
# def test_main(mock_requests, mock_datetime, mock_sleep, mock_email_send):
#     _get = mock.Mock(side_effect=[
#         mock.Mock(url='https://www.economist.com/printedition/2019-03-01'),
#         mock.Mock(url='https://www.economist.com/printedition/2019-03-08'),
#     ])
#     mock_requests.return_value = mock.Mock(get=_get)

#     dt = mock.Mock(today=lambda: datetime.date(2019, 3, 8),
#                    now=lambda: datetime.datetime(2019, 3, 8, 16, 30))
#     mock_datetime.return_value = dt

#     # mock_sleep.return_value = mock.Mock(lambda: 0)

#     economist_updated.main()
#     mock_email_send.assert_called_with(
#         'New Economist', 'A new Economist has been released: 2019-03-08')


def main():
    filename = os.path.basename(__file__)
    pytest.main([filename])


if __name__ == '__main__':
    main()
