from bs4 import BeautifulSoup
import requests as req
from urllib.parse import urljoin
import json
import threading

links = json.loads(open("config.json").read())["links"]


out = """%%%\n"""


def get_hrefs(url: str) -> list:
    html = req.get(url).text
    parsed = BeautifulSoup(html, "html.parser").find_all("a", href=True)

    return [
        urljoin(url, x["href"]) if "https://" not in x["href"] else x["href"]
        for x in parsed
    ]


def href_to_html(url) -> str:
    return BeautifulSoup(req.get(url).text, "html.parser").get_text()


llen = len(links)
lcount = 1

for link in links:
    print(f"Scraping: {link}")
    hrefs = get_hrefs(link)

    hlen = len(hrefs)
    hcount = 1

    for href in hrefs:
        print(f"{hcount}/{hlen}")
        out += f"{(href_to_html(href))}\n%%%"
        hcount += 1

    lcount += 1

    with open(f"Files/link-{lcount}.txt", "w", encoding="utf-8") as file:
        file.write(out)

print("Finished")
input()
