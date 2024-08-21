import requests as rq
import bs4 as _bs

def _get_page(url: str):
    response = rq.get(url)
    return _bs.BeautifulSoup(response.content, "html.parser")

