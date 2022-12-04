import html
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import re
import shutil


REVIEW_URL = "https://www.breakingbourbon.com/review/seelbachs-private-reserve-straight-bourbon-finished-in-triple-sec-and-sparkling-wine-barrels"
FIRST_REVIEW = "https://www.breakingbourbon.com/review/george-t-stagg-2013-release"
IMG_REGEX = r"(https?:\/\/.*\.(?:png|jpg))"
REGEX_FLAGS = re.MULTILINE | re.IGNORECASE


def retrieve_image_from_page(url_str, data_path: Path = Path("."), download=True):
    page = requests.get(url_str)
    soup = BeautifulSoup(page.content, 'html.parser')
    main_photo_section = soup.find_all("div", {"class": "main-photo-section"})
    matches = re.findall(IMG_REGEX, str(main_photo_section), re.MULTILINE)
    r = requests.get(matches[0], stream=True)
    filename = matches[0].split("/")[-1]

    if download:
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(data_path / filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    return filename


def clean_text(regex, text, flags):
    finding = re.findall(regex, text, flags=flags)
    if len(finding) > 0:
        output = finding[0].encode('ascii', errors='ignore').decode('utf8')
        output = output.replace("&nbsp;", "")
        output = html.unescape(output)

        return output
    else:
        return None


class BBData:
    def __init__(self, review_url, rating):
        self.review_url = review_url

        page_text = requests.get(self.review_url).text

        title = clean_text(r"<h1 class=\"bold-page-title.*?>(.*?)<\/h1", page_text, flags=REGEX_FLAGS)
        category = clean_text(r"<h2 class=\"category\">(.*?)<\/h2>", page_text, flags=REGEX_FLAGS)
        classification = clean_text(r"classification.*?<\/strong>:?(.*?)<\/p>", page_text, flags=REGEX_FLAGS)
        company = clean_text(r"company.*?<\/strong>:?(.*?)<\/p>", page_text, flags=REGEX_FLAGS)
        distillery = clean_text(r"distillery.*?<\/strong>:?(.*?)<\/p>", page_text, flags=REGEX_FLAGS)
        release_date = clean_text(r'(?:released|release.*?date).*?<\/strong>:?(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        proof = clean_text(r'proof.*?<\/strong>:?(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        age = clean_text(r'age.*?<\/strong>:?(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        mashbill = clean_text(r'mashbill.*?<\/strong>:?(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        color = clean_text(r'color.*?<\/strong>:?(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        msrp = clean_text(r'msrp|price.*?<\/strong>:?.*?\$([\d|,]+(?:.\d+)?)', page_text, flags=REGEX_FLAGS)
        nose = clean_text(r'palate<\/div>.*?<p>(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        palate = clean_text(r'palate<\/div>.*?<p>(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        finish = clean_text(r'finish<\/div>.*?<p>(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        overall = clean_text(r'overall<\/div>.*?<p>(.*?)<\/p>', page_text, flags=REGEX_FLAGS)
        image_filename = retrieve_image_from_page(review_url, Path("data/images"), download=True)

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
            'overall': overall,
            'image_filename': image_filename,
            'rating': rating
        }


def main():
    out = []
    df = pd.read_csv("data/review_url_reference.csv")
    for idx, row in df.iterrows():
        D = BBData(review_url=row['review_url'], rating=row['rating'])
        print(D.data)
        out.append(D.data)

    out_df = pd.DataFrame(out)
    out_df.to_csv("data/review_data.csv")


if __name__ == "__main__":
    main()
