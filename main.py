from bs4 import BeautifulSoup
import requests as req
from urllib.parse import urljoin
import json
import threading
from datetime import datetime

links = json.loads(open("config.json").read())["links"]

start = datetime.now()

out = """%%%\n"""


def get_hrefs(url: str) -> list:
    html = req.get(url).text
    parsed = BeautifulSoup(html, "html.parser").find_all("a", href=True)

    return [
        urljoin(url, x["href"]) if "https://" not in x["href"] else x["href"]
        for x in parsed
    ]


def get_link(link_):
    hrefs = get_hrefs(link_)
    print(f"Found {len(hrefs)} links")
    threads = []
    for href in hrefs:
        thread = threading.Thread(target=get_text_from_href, args=(href,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def get_text_from_href(href):
    with open("output.html", "a", encoding="utf-8") as file_:
        file_.write(f"{BeautifulSoup(req.get(href).content, 'html.parser').find('body')}\n\n\n%%%\n\n\n")
    print(f"Parsed: {href}")
    return


for link in links:
    get_link(link)

end = datetime.now()

delt = end - start
print(f"Finished in {delt.seconds} seconds!")
