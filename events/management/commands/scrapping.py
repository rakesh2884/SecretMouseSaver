from bs4 import BeautifulSoup
from selenium import webdriver
import time
from secretmousesaver.settings import URL, IMAGE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from datetime import timedelta
from events.models import Event
from datetime import datetime, date
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'scrapping the data'

    def handle(self, *args, **options):
        google_search = self.scrape_google_search(URL)
        for link in google_search:
            print(link)
            self.get_data(link)

    def scrape_google_search(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        scroll_pause_time = 2
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1
        while True:
            driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = \
                driver.execute_script("return document.body.scrollHeight;")
            if screen_height * i > scroll_height:
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, "//a[@aria-label='More results']"
                        ))
                    )
                    next_button.click()
                    time.sleep(5)
                except Exception:
                    break
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.find_all(attrs={"jsname": "UWckNb"})
        urls = [link['href'] for link in links]
        driver.quit()
        print(len(urls))
        return urls

    def get_data(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        scroll_pause_time = 2
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1
        while True:
            driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = \
                driver.execute_script("return document.body.scrollHeight;")
            if screen_height * i > scroll_height:
                break
        soup = BeautifulSoup(driver.page_source, "html.parser")
        event_headline = soup.select(".info-banner--first-inline")
        event_dates = soup.select(".info-banner--second-inline")
        try:
            image_to_ignore = \
                soup.find_all(attrs={"src": IMAGE})
        finally:
            for headline in event_headline:
                eventBanner = headline.getText()
                try:
                    eventBanner = headline.getText().split(': ')[-1]
                finally:
                    eventBanner = eventBanner
            for dates in event_dates:
                eventDates = dates.getText()
                try:
                    eventDates = eventDates.split(': ')[-1]
                finally:
                    eventStartDate = datetime.strptime(
                        eventDates.split(' - ')[0],
                        '%b %d, %Y'
                    ).date()
                    eventEndDate = datetime.strptime(
                        eventDates.split(' - ')[1],
                        '%b %d, %Y'
                    ).date()
                    days = timedelta(days=7)
            if event_headline and event_dates:
                if eventStartDate > date.today() and not image_to_ignore:
                    event, created = \
                        Event.objects.get_or_create(
                            eventBanner=eventBanner,
                            eventPageURL=url,
                            eventStartDate=eventStartDate,
                            eventEndDate=eventEndDate,
                            validStartDate=eventStartDate - days,
                            validEndDate=eventEndDate + days
                        )
                    driver.quit()
                else:
                    driver.quit()
            else:
                driver.quit()
