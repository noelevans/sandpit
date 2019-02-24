import bs4
import html2text
import re
import requests


def run(url):
    resp = requests.get(url)
    html_text = resp.text
    soup = bs4.BeautifulSoup(html_text, 'html.parser')

    tag_names = ['script', 'noscript', 'title', 'iframe', 'cf_floatingcontent',
                 'aside', 'footer']
    for t in tag_names:
        for el in soup.find_all(t):
            el.extract()

    tag_classes = [
        'dblClkTrk', 'ec-article-info', 'share_inline_header',
        'related-items', 'main-content-container', 'ec-topic-widget',
        'teaser', 'blog-post__bottom-panel-bottom',
        'blog-post__comments-label', 'blog-post__foot-note',
        'blog-post__sharebar', 'blog-post__bottom-panel',
        'newsletter-form','share-links-header','teaser--wrapped',
        'latest-updates-panel__container',
        'latest-updates-panel__article-link','blog-post__section',
        ('latest-updates-panel__container latest-' +
            'updates-panel__container--blog-post'),
        'ribbon__body-slider-item-desc']
    for t in tag_names:
        for el in soup.find_all(class_=t):
            el.extract()

    omits = ['Upgrade your inbox and get', 'Join them. ',
             'or Sign up to continue reading ']
    all_paragraphs = [p.get_text() for p in soup.find_all('p')]
    paragraphs = []
    for p in  all_paragraphs:
        if not any(p.startswith(o) for o in omits):
            paragraphs.append(p)

    title = soup.find('h1').get_text()
    return title + '\n\n\n' + '\n\n'.join(paragraphs)


def main():
    url = ('https://www.economist.com/obituary/2019/02/16/' +
        'obituary-james-mcmanus-died-on-february-4th')
    print(run(url))

if __name__ == '__main__':
    main()
