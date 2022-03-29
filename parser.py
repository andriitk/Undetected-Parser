from bs4 import BeautifulSoup
# from selenium import webdriver
# from random_user_agent import user_agent
import undetected_chromedriver
import time
import requests

URL = f"https://www.sravni.ru/banki/rating/kredity-fizicheskikh-lic/?ratingType=Credit&startPeriod=2021" \
      f"-04-01&endPeriod=2021-05-01&page=1&sortBy=&isAscSort=false&locationAlias=&allRecords=false"

URL_0 = 'https://www.sravni.ru'


# PATH = r'c:\Program Files (x86)\chromedriver.exe'
# options = webdriver.ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument(f"user-agent={user_agent}")
# options.headless = True
# options.add_argument("--headless")


def get_start_html_file_with_selenium(url):
    # Записываем HTML-код в файл
    # driver = webdriver.Chrome(PATH, options=options)
    driver = undetected_chromedriver.Chrome()  # Для CloudFlare
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(10)

        with open("index_selenium.html", "w") as file:
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
    with open("index_selenium.html") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    count_pages = len(soup.find("div", class_="pagination").find_all("li", class_="item"))
    return count_pages


def all_data_with_files(count_pages: int):
    for i in range(1, count_pages + 1):
        #     URL = f"https://www.sravni.ru/banki/rating/kredity-fizicheskikh-lic/?ratingType=Credit&startPeriod=2021" \
        #           f"-04-01&endPeriod=2021-05-01&page={i}&sortBy=&isAscSort=false&locationAlias=&allRecords=false"
        #     driver = undetected_chromedriver.Chrome()  # Для CloudFlare
        #     driver.maximize_window()
        #
        #     try:
        #         driver.get(URL)
        #         time.sleep(10)
        #
        #         with open(f"index_selenium_{i}.html", "w") as file:
        #             file.write(driver.page_source)
        #
        #     except Exception as ex:
        #         print(ex)
        #     finally:
        #         driver.close()
        #         driver.quit()

        with open(f"index_selenium_{i}.html") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")

        blocks = soup.find("table", class_="ratings-table ratings-table--column ratings-table--white-header "
                                           "ratings-table--adaptive-2").find("tbody").find_all("tr")

        for link in blocks:
            link = link.find("a", class_="link").get("href")
            with open('link.txt', 'a+', encoding='utf-8') as f:
                f.write(f"{URL_0}{link}\n")


def main():
    # get_start_html_file_with_selenium(URL)
    all_data_with_files(count_pages())


if __name__ == '__main__':
    main()
