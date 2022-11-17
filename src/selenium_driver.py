import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

HOMEPAGE_URL = (
    "https://www.breakingbourbon.com/bourbon-rye-whiskey-reviews-sort-by-rating"
)
PATIENCE_TIME = 60
START_XPATH = "/html/body/div[1]/div/div/div[2]/a[1]"
LOAD_MORE_BUTTON_XPATH = "/html/body/div[7]/div/div[1]/div[2]/div/div/div[2]/a[2]"


def click_load_more(browser: webdriver, click_counter: int = 0):
    while True:
        try:
            load_more_button = browser.find_element(
                By.XPATH,
                value="//*[@aria-label='Next Page' and not(ancestor::*[contains(@style, 'display: none')]) and ancestor::*[contains(@class, 'w--tab-active')]]",
            )
            load_more_button.click()
            click_counter += 1
        except Exception as e:
            print(e)
            break

    return click_counter


def get_bb_review_list(url: str):
    browser = webdriver.Firefox()
    browser.get(url)
    click_counter = 0

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

        click_counter = click_load_more(browser, click_counter)

        # second element is list, first is rating button
        level = browser.find_element(
            By.XPATH,
            value=f"//*[@data-w-tab='Tab {idx+1}' and contains(@class, 'w-tab-pane')]",
        )
        time.sleep(1)
        reviews = level.find_elements(
            By.XPATH,
            value=f".//child::a[contains(@class, 'w-inline-block') and contains(@href, 'review/') and child::*[contains(@style, 'background')]]",
        )
        for review in reviews:
            review_levels.append((review.get_attribute("href"), rating_levels[idx]))

    browser.quit()

    return review_levels


def main():
    reviews = get_bb_review_list(HOMEPAGE_URL)
    review_url_df = pd.DataFrame(reviews)
    print(len(review_url_df.index))


if __name__ == "__main__":
    main()
