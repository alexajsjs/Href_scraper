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


def get_link(link):
    hrefs = get_hrefs(link)
    print(f"Found {len(hrefs)} links")
    threads = []
    for href in hrefs:
        thread = threading.Thread(target=get_text_from_href, args=(href,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def get_text_from_href(href):
    global out
    out += f"{BeautifulSoup(req.get(href).text, 'html.parser').get_text()}\n%%%"
    print(f"thread done!")
    return


for link in links:
    get_link(link)
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(out)
    out = ""

end = datetime.now()

delt = end - start
print(f"Finished in {delt.seconds} seconds!")
