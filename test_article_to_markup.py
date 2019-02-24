from unittest import mock
import os
import pytest
import re

import article_to_markup


@mock.patch('article_to_markup.requests.get')
def test_html(mock_get):
    with open('sample_article.html') as f:
        mock_get.return_value = mock.Mock(text=f.read().replace('\n', ''))

    html = article_to_markup.html('http://fake-url.com')

    # print(html)
    latest_updates = ('latest-updates-panel__container latest-' +
        'updates-panel__container--blog-post')

    assert html.split('\n')

    for line in html.split('\n'):
        assert not re.search(latest_updates, line)


def main():
    filename = os.path.basename(__file__)
    pytest.main([filename])


if __name__ == '__main__':
    main()
