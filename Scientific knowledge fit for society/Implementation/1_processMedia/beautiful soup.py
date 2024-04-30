from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(soup):
    # texts = soup.findAll(text=True)
    # visible_texts = filter(tag_visible, texts)  
    # return u" ".join(t.strip() for t in visible_texts)
    return soup.get_text()

def title_from_html(soup):
    title = soup.title.string
    return title

def get_all_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def get_web_media_with_url(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    text = text_from_html(soup)
    title = title_from_html(soup)
    return (text, title)


