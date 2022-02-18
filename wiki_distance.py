import typing as tp
import requests
from bs4 import BeautifulSoup


def distance(source_url: str, target_url: str) -> tp.Optional[int]:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
    wiki_url = "https://ru.wikipedia.org"
    urls = []

    def recursive_distance(source_url: str, target_url: str, urls: tp.List[str]) -> tp.Optional[int]:
        if source_url == target_url:
            return len(urls) - 1
        html = requests.get(source_url).text
        soup = BeautifulSoup(html, "html.parser")
        wiki_as = soup.find("div", attrs={"class": "mw-parser-output"}).find("p", recursive=False).find_all("a")
        new_url = None
        for wiki_a in wiki_as:
            if "title" not in wiki_a.attrs:
                continue
            title = wiki_a["title"]
            if 'href' not in wiki_a.attrs:
                continue
            if '#' in wiki_a['href']:
                continue
            if '.' in wiki_a['href']:
                continue
            if '/wiki/' not in wiki_a['href']:
                continue
            url = wiki_a
            new_url = wiki_url + url['href']
            if new_url not in urls:
                urls.append(new_url)
                print(title, len(urls) + 1)
                break
        if urls and new_url:
            recursive_distance(new_url, target_url, urls)

    recursive_distance(source_url, target_url, urls)
    if urls:
        print(f"length is {len(urls)}")
    return len(urls) if urls else None


if __name__ == "__main__":

    distance("https://ru.wikipedia.org/wiki/Linux",
             "https://ru.wikipedia.org/wiki/%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0")
