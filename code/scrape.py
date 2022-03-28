import time

import requests
from bs4 import BeautifulSoup


def extract_price(div_tag):
    """Gets the price from a "result-info" div."""
    span_tags = div_tag.find_all("span", class_="result-price")

    if not span_tags:
        return None

    return int(
        div_tag.find_all("span", class_="result-price")[0]
        .text.replace("$", "")
        .replace(",", "")
    )


def extract_item(div_tag):
    """Gets the item information from a "result-info" div."""

    a_tag = div_tag.find_all("a", class_="result-title")[0]

    time = div_tag.find_all("time")[0]["datetime"]
    price = extract_price(div_tag)
    title = a_tag.text
    link = a_tag["href"]
    post_id = a_tag["id"]

    return {
        "time": time,
        "price": price,
        "title": title,
        "link": link,
        "post_id": post_id,
    }


def extract_items(div_tags):
    """Gets the items from a list of "result-info" div tags."""

    return [extract_item(div_tag) for div_tag in div_tags]


def request_page(page_num, query):
    """Request a page starting at page 0 and get a list of items."""

    offest = page_num * 120

    base_url = "https://austin.craigslist.org/search/sss"

    params = {"s": offest, "query": query}

    response = requests.get(base_url, params=params)

    response.raise_for_status()

    soup = BeautifulSoup(response.text)

    div_tags = soup.find_all("div", class_="result-info")

    return extract_items(div_tags)


def request_pages(query):
    """Request all pages and get a list of items."""

    page_num = 0

    items = []

    while True:

        new_items = request_page(page_num, query)

        if not new_items:
            break

        items += new_items

        page_num += 1

        time.sleep(1)

    return items


if __name__ == "__main__":
    request_pages("piano")
