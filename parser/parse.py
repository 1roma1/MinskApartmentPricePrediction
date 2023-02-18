import os
import json
import requests

from multiprocessing import Pool
from datetime import date
from bs4 import BeautifulSoup


URL = "https://realt.by/sale/flats/?search=eJwryS%2FPi89MUTV1SlU1dbE1NTQwAgBBKAWZ"
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36" \
             "(KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36"
HEADERS = {'user-agent': USER_AGENT,
           'accept': '*/*'}


def request_html(url, headers, params=None):
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code==200:
        return resp


def get_pages_count(url, headers):
    resp = request_html(url, headers)
    if resp != None:
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find('div', class_='pagination')
        num_pages = int(items.find(
                'ul').find_all('li')[-1].get_text())
        return num_pages
    else:
        print(f"Error in page count parsing. Status code {resp.status_code}")


def get_page_links(url, num_pages):
    page_links = []
    for i in range(0, num_pages):
        page_link = url if i == 0 else url+f'&page={i}'
        page_links.append(page_link)
    return page_links


def parse_links(url, headers=HEADERS):
    resp = request_html(url, headers)
    links = []
    if resp != None:
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.find_all('div', class_='showcase-objects-item')
        for item in items:
            link = item.find('a').get('href')
            if "https" in link:
                links.append(link)
    else:
        print(f"Error in parsing {url}")
    return links


def parse_flat_info(url, headers=HEADERS):
    resp = request_html(url, headers)
    if resp != None:
        soup = BeautifulSoup(resp.text, 'html.parser')

        json_text = soup.find('script', {"id": "__NEXT_DATA__"}).get_text()
        json_info = json.loads(json_text)

        return json_info
    else:
        print(f"Error in parsing {url}")
        return {}


if __name__ == "__main__":
    num_pages = get_pages_count(URL, HEADERS)
    if num_pages != None:
        print(f"Pages count: {num_pages}")

        page_links = get_page_links(URL, num_pages)
        with Pool(10) as p:
            link_lists = p.map(parse_links, page_links)
        print(f"Links are successfully parsed")
        
        # from [[], [], ..., []] to [...]
        links = []
        for link_list in link_lists:
            for link in link_list:
                links.append(link)

        print(f"Links count: {len(links)}")

        dir_name = os.path.join("data", str(date.today()).replace("-", "_"))
        os.makedirs(dir_name, exist_ok=True)
        for i in range(0, len(links), 1000):
            links_slice = links[i:i+1000] if i+1000 < len(links) else links[i:]

            with Pool(10) as p:
                flats_info = p.map(parse_flat_info, links_slice)
            if i+1000 < len(links): 
                print(f"{i+1000} links are parsed")
            else:
                print(f"{len(links)} links are parsed")

            file_name = f"{i}_{i+1000}.json" if i+1000 < len(links) else f"{i}_{len(links)}.json"
            with open(os.path.join(dir_name, file_name), "w", encoding="utf-8") as f:
                json.dump(flats_info, f)
