import requests
from bs4 import BeautifulSoup


REVIEW_URL = "https://www.breakingbourbon.com/review/seelbachs-private-reserve-straight-bourbon-finished-in-triple-sec-and-sparkling-wine-barrels"


def main():
    page = requests.get(REVIEW_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.prettify())
    # print(soup.find_all(class_="w-dyn-list"))


if __name__ == "__main__":
    main()
