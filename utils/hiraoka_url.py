import requests as rq
import bs4 as _bs

url_hiraoka = "https://hiraoka.com.pe"

def _url_brand(brand: str, page: int = 1) -> str:
    return f"{url_hiraoka}/marca-{brand}?p={page}"

def _get_page(url: str) -> _bs.BeautifulSoup:
    response = rq.get(url)
    return _bs.BeautifulSoup(response.content, "html.parser")