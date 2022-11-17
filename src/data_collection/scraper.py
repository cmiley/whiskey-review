import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


REVIEW_URL = "https://www.breakingbourbon.com/review/seelbachs-private-reserve-straight-bourbon-finished-in-triple-sec-and-sparkling-wine-barrels"
FIRST_REVIEW = "https://www.breakingbourbon.com/review/george-t-stagg-2013-release"

class BBData:
    def __init__(self, review_url):
        self.review_url = review_url

        page_text = requests.get(self.review_url).text

        title = re.findall(r"<h1 class=\"bold-page-title.*?>(.*?)<\/h1", page_text, flags=re.IGNORECASE)
        category = re.findall(r"<h2 class=\"category\">(.*?)<\/h2>", page_text, flags=re.IGNORECASE)
        classification = re.findall(r"classification.*?<\/strong>:?(.*?)<\/p>", page_text, flags=re.IGNORECASE)
        company = re.findall(r"company.*?<\/strong>:?(.*?)<\/p>", page_text, flags=re.IGNORECASE)
        distillery = re.findall(r"distillery.*?<\/strong>:?(.*?)<\/p>", page_text, flags=re.IGNORECASE)
        release_date = re.findall(r'(?:released|release date).*?<\/strong>:?(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        proof = re.findall(r'proof.*?<\/strong>:?(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        age = re.findall(r'age.*?<\/strong>:?(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        mashbill = re.findall(r'mashbill.*?<\/strong>:?(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        color = re.findall(r'color.*?<\/strong>:?(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        msrp = re.findall(r'/msrp.*?<\/strong>:?.*?(\$[\d|,]+(?:\.\d+)?)/gm', page_text, flags=re.IGNORECASE)
        nose = re.findall(r'palate<\/div>.*?<p>(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        palate = re.findall(r'palate<\/div>.*?<p>(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        finish = re.findall(r'finish<\/div>.*?<p>(.*?)<\/p>', page_text, flags=re.IGNORECASE)
        overall = re.findall(r'overall<\/div>.*?<p>(.*?)<\/p>', page_text, flags=re.IGNORECASE)

        self.data = {
            'title': title,
            'category': category,
            'classification': classification,
            'company': company,
            'distillery': distillery,
            'release_date': release_date,
            'proof': proof,
            'age': age,
            'mashbill': mashbill,
            'color': color,
            'msrp': msrp,
            'nose': nose,
            'palate': palate,
            'finish': finish,
            'overall': overall
        }


def main():
    out = []
    df = pd.read_csv("data/review_url_reference.csv")
    for idx, row in df.iterrows():
        D = BBData(review_url=row['review_url'])
        print(D.data)
        out.append(D.data)

    out_df = pd.DataFrame(out).to_csv("data/review_data.csv")


if __name__ == "__main__":
    main()
