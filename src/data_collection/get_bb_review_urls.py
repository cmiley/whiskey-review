import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

HOMEPAGE_URL = (
    "https://www.breakingbourbon.com/bourbon-rye-whiskey-reviews-sort-by-rating"
)


def click_load_more(browser: webdriver):
    while True:
        try:
            load_more_button = browser.find_element(
                By.XPATH,
                value="//*[@aria-label='Next Page' and not(ancestor::*[contains(@style, 'display: none')]) and ancestor::*[contains(@class, 'w--tab-active')]]",
            )
            load_more_button.click()
        except Exception as e:
            break


def get_bb_review_list(url: str):
    browser = webdriver.Firefox()
    browser.get(url)

    # click Yes on over 21 popup
    top_button = browser.find_element(By.XPATH, value="//*[contains(text(),'YES')]")
    top_button.click()

    # in reverse order
    rating_levels = ["5", "4.5", "4", "3.5", "3", "2.5", "2", "1.5", "1", "0.5"]
    review_levels = []

    # click through each review level
    review_buttons = browser.find_elements(By.CLASS_NAME, value="barrel-rating-button")
    for idx, button in enumerate(review_buttons):
        button.click()

        click_load_more(browser)

        # get parent element
        level = browser.find_element(
            By.XPATH,
            value=f"//*[@data-w-tab='Tab {idx+1}' and contains(@class, 'w-tab-pane')]",
        )

        # get each review element
        reviews = level.find_elements(
            By.XPATH,
            value=f".//child::a[contains(@class, 'w-inline-block') and contains(@href, 'review/') and child::*[contains(@style, 'background')]]",
        )

        for review in reviews:
            review_levels.append(
                {
                    "review_url": review.get_attribute("href"),
                    "rating": rating_levels[idx],
                }
            )

    browser.quit()

    return review_levels


def main():
    reviews = get_bb_review_list(HOMEPAGE_URL)
    review_url_df = pd.DataFrame(reviews)
    review_url_df.to_csv("data/review_url_reference.csv")


if __name__ == "__main__":
    main()
