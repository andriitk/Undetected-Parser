from bs4 import BeautifulSoup
# from selenium import webdriver
# from random_user_agent import user_agent
from concurrent.futures import ProcessPoolExecutor
import undetected_chromedriver as uc
import time
import os
import requests

URL = f"https://www.sravni.ru/banki/rating/kredity-fizicheskikh-lic/?ratingType=Credit&startPeriod=2021" \
      f"-04-01&endPeriod=2021-05-01&page=1&sortBy=&isAscSort=false&locationAlias=&allRecords=false"

URL_0 = 'https://www.sravni.ru'


# PATH = r'c:\Program Files (x86)\chromedriver.exe'
# options = webdriver.ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument(f"user-agent={user_agent}")


def get_start_html_file_with_selenium(url):
    # Записываем HTML-код в файл
    # driver = webdriver.Chrome(PATH, options=options)
    driver = uc.Chrome()  # Для CloudFlare
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(10)

        with open("templates/index_selenium.html", "w", encoding='utf-8') as file:
            file.write(driver.page_source)
            return True

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    return False


def count_pages():
    # Забираем количество страниц
    with open("templates/index_selenium.html", 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    count_pages = len(soup.find("div", class_="pagination").find_all("li", class_="item"))

    return count_pages


def all_data_with_files(count_pages: int):
    path = "templates"
    filelist = []

    for i in range(1, count_pages + 1):
        URL = f"https://www.sravni.ru/banki/rating/kredity-fizicheskikh-lic/?ratingType=Credit&startPeriod=2021" \
              f"-04-01&endPeriod=2021-05-01&page={i}&sortBy=&isAscSort=false&locationAlias=&allRecords=false"
        driver = uc.Chrome()  # Для CloudFlare
        driver.maximize_window()

        try:
            driver.get(URL)
            time.sleep(10)

            with open(f"./templates/index_selenium_{i}.html", "w", encoding='utf-8') as file:
                file.write(driver.page_source)

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(file)

    return filelist


def parse_with_template(path_to_file: str):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    blocks = soup.find("table", class_="ratings-table ratings-table--column ratings-table--white-header "
                                       "ratings-table--adaptive-2").find("tbody").find_all("tr")
    return blocks


def parse_links(blocks: list):
    for link in blocks:
        link = link.find("a", class_="link").get("href")
        linkk = f"{URL_0}{link}"

        # options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument('--headless')

        driver = uc.Chrome()  # Для CloudFlare
        # driver.maximize_window()

        try:
            driver.get(url=linkk)
            time.sleep(15)

            with open(f"./temp_with_links/link.html", 'w', encoding='utf-8') as f:
                f.write(driver.page_source)

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

        with open(f"./temp_with_links/link.html", 'r', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")

        try:
            block = soup.find_all("div", class_="sc-10ef58l-0 eDwFaN")[4]
            url = block.find("a", class_="t-link").get('href')
            with open("links.txt", 'a+', encoding='utf-8') as f:
                f.write(f"{url}\n")
            # time.sleep(3)
        except IndexError:
            block = soup.find_all("div", class_="sc-10ef58l-0 eDwFaN")[5]
            url = block.find("a", class_="t-link").get('href')
            with open("links.txt", 'a+', encoding='utf-8') as f:
                f.write(f"{url}\n")


def main():
    # 1  get_start_html_file_with_selenium(URL)
    filelist = all_data_with_files(count_pages())
    for i in filelist:
        blocks = parse_with_template(i)
        parse_links(blocks)


if __name__ == '__main__':
    main()
