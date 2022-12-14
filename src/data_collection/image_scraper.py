from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import shutil
from pathlib import Path
from scraper import IMG_REGEX

def main():
    page = requests.get("https://www.breakingbourbon.com/review/barrell-bourbon-batch-031")
    soup = BeautifulSoup(page.content, 'html.parser')
    main_photo_section = soup.find_all("div", {"class": "main-photo-section"})
    matches = re.findall(IMG_REGEX, str(main_photo_section), re.MULTILINE)
    r = requests.get(matches[0], stream=True)
    filename = matches[0].split("/")[-1]

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')


if __name__ == "__main__":
    main()
