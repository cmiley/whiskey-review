from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#browser = webdriver.Firefox()#Chrome('./chromedriver.exe')
HOMEPAGE_URL = "https://www.breakingbourbon.com/bourbon-rye-whiskey-reviews-sort-by-review-date"
PATIENCE_TIME = 60
START_XPATH = '/html/body/div[1]/div/div/div[2]/a[1]'
LOAD_MORE_BUTTON_XPATH = '/html/body/div[7]/div/div[1]/div[2]/div/div/div[2]/a[2]'


def main():
    browser = webdriver.Firefox()
    browser.get(HOMEPAGE_URL)
    print("Got homepage url")
    click_counter = 0
    top_button = browser.find_element(By.XPATH, value="//*[contains(text(),'YES')]")
    top_button.click()

    while True:
        try:
            load_more_button = browser.find_element(By.XPATH, value="//*[@aria-label='Next Page']")
            load_more_button.click()
            click_counter += 1
            print(f"clicked: {click_counter}")
        except Exception as e:
            print(e)
            break
    reviews = [review.get_attribute('href') for review in browser.find_elements(By.XPATH, value="//*[contains(@href, 'review/') and contains(@class, 'link-block')]")]
    print(f"Found {len(reviews)} Reviews")
    browser.quit()


if __name__ == "__main__":
    main()
