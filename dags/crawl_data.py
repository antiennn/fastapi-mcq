import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from redis_config import redis_client

def crawl_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # <-- chạy ẩn
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)

    driver.get('https://study4.com/topics/tu-vung/')

    time.sleep(2)

    posts_list = driver.find_element(By.CLASS_NAME, 'posts-list')

    cards = posts_list.find_elements(By.CLASS_NAME, 'postlist-card')

    first_card = cards[4]

    content_wrapper = first_card.find_element(By.CLASS_NAME,
                                              'postlist-card-content-wrapper')

    title_wrapper = content_wrapper.find_element(By.CLASS_NAME,
                                                 'postlist-title-wrapper')

    title = title_wrapper.find_element(By.CLASS_NAME, 'postlist-title')

    link = title.find_element(By.TAG_NAME, 'a')

    href = link.get_attribute('href')

    if redis_client.sismember('post_links_set', href):
        print(f"Link {href} have crawled to csv.")
    else:
        redis_client.sadd('post_links_set', href)

        driver.get(href)

        time.sleep(2)

        tables = driver.find_elements(By.TAG_NAME, 'table')

        csv_filename = 'vocab_list.csv'

        if not os.path.exists(csv_filename):
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

        vocab_count = 0

        for table in tables:

            rows = table.find_elements(By.TAG_NAME, 'tr')

            if not rows:
                continue

            headers = rows[0].find_elements(By.TAG_NAME, 'th')
            if not headers:
                headers = rows[0].find_elements(By.TAG_NAME, 'td')

            vocab_col_idx = None
            for idx, header in enumerate(headers):
                if "từ vựng" in header.text.lower():
                    vocab_col_idx = idx
                    break

            if vocab_col_idx is None:
                continue

            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if len(cols) > vocab_col_idx:
                    vocab_word = cols[vocab_col_idx].text.strip()
                    if vocab_word:
                        with open(csv_filename, mode='a', newline='',
                                  encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow([vocab_word])
                        vocab_count += 1

                        if vocab_count >= 10:
                            break

    driver.quit()
