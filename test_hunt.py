import requests
import re
import bs4
from bs4 import BeautifulSoup


def main():
    url_home = "https://news.abs-cbn.com/"
    soup_list = soup_getter(url_home)


def soup_getter(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Try again.")

    home_soup = BeautifulSoup(html_content, 'html.parser')
    results = home_soup.find_all('article')

    trial = results[138]
    match = re.search(r'href="(.+)"', str(trial))
    if match:
        a = match.group(1)
        print(a)
    else:
        print("no match")


if __name__ == "__main__":
    main()
