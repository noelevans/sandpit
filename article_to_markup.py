import bs4
import html2text
import re
import requests


def html(url):
    resp = requests.get(url)
    html = resp.text
    soup = bs4.BeautifulSoup(html, 'html.parser')

    clazz = ('latest-updates-panel__container latest-' +
        'updates-panel__container--blog-post')
    soup.find('div', class_=clazz).extract()

    return str(soup)


def markdown(html):
    page_md = html2text.html2text(html)

    reached_start = False
    result = ''
    icons = [el + ' icon' for el in
        ['linkedin', 'facebook', 'twitter', 'mail', 'print']]
    omissions = icons + [
        'Get our daily newsletter',
        'Upgrade your inbox and get '

        ]


    for line in page_md.split('\n'):
        if reached_start or re.match(r'^#\  \w', line):
            reached_start = True
            if not any(omit in line for omit in omissions):
                result += line + '\n'

    return result


def main():
    url = ('https://www.economist.com/obituary/2019/02/16/' +
        'obituary-james-mcmanus-died-on-february-4th')
    print(run(url))

if __name__ == '__main__':
    main()
