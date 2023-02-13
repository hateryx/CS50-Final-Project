import requests
import re
import titlecase
from bs4 import BeautifulSoup
import random

from reportlab.pdfgen import canvas

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame


def main():
    inquire_input = input(
        "Please select from the following: \n 1 - Business \n 2 - Headline News \n 3 - Showbiz \n: ")
    if inquire_input == "1":
        url = ("https://news.abs-cbn.com/business")
        soup_list = soup_getter(url, "business")
    if inquire_input == "2":
        url = "https://news.abs-cbn.com/news"
        soup_list = soup_getter(url, "news")
    if inquire_input == "3":
        url = "https://news.abs-cbn.com/entertainment"
        soup_list = soup_getter(url, "entertainment")
    pick = random.choice(soup_list)
    final_url = "https://news.abs-cbn.com"+pick
    print(final_url)

    title = title_builder(str(pick))
    content = content_getter(final_url)
    news_pdf = generate_news_pdf(title, content)


def soup_getter(url, type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Try again later.")

    home_soup = BeautifulSoup(html_content, 'html.parser')
    results = home_soup.find_all('article')

    news_list = []

    for result in results:
        match = re.search(r'href="(/'+type+'/\d{2}/.+)">{1}', str(result))
        if match:
            if match.group(1) not in news_list:
                news_list.append(match.group(1))
    return news_list


def content_getter(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Try again later.")

    content_list = []

    content_soup = BeautifulSoup(html_content, 'html.parser')
    content_maker = content_soup.find_all("p")
    for line in content_maker:
        match = re.search(r"<p>(.+)</p>", str(line))
        if match:
            if match.group(1) != "Share":
                content_list.append(match.group(1))
    return content_list


def title_builder(title):
    match = re.search(r"/.+/(\d{2}/\d{2}/\d{2}/)(.+)", title)
    if match:
        date = match.group(1)
        snippet = match.group(2)
    x = snippet.replace("-", " ")
    f_title = titlecase.titlecase(x)

    return f_title


def generate_news_pdf(title, contents):

    fileName = "news_x.pdf"
    create_content = " <br/><br />".join(contents)

    pdf = canvas.Canvas(fileName)
    pdf.setTitle(title)
    pdf.drawString(40, 815, title)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    story = []
    # add some flowables
    story.append(Paragraph(create_content, styleN))

    f = Frame(inch, inch, 6*inch, 10*inch, showBoundary=1)
    f.addFromList(story, pdf)
    pdf.save()


if __name__ == "__main__":
    main()
