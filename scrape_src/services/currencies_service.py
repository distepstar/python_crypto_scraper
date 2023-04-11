# threading
from queue import Queue
from threading import Thread

# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# modules
from .. import selenium_driver
# consts
from ..consts import urls
from ..models import currencies_model
from ..utils import pandas_utils


class OverviewThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            try:
                driver = selenium_driver.get_chrome_driver()
                driver.get(url)
                print(f"Searching: {url}")
                currency_eles = driver.find_elements(By.CLASS_NAME, "css-vlibs4")
                get_currency_data_overview(currency_eles)
                driver.close()
            finally:
                self.queue.task_done()


def get_currency_overview(threads=4):
    get_currency_overview_thread(threads)


def get_currency_overview_thread(threads):
    # get urls by it's pages
    fetch_urls = get_currency_overview_urls()
    # creating temp queue for threads pooling
    queue = Queue()
    # creating threads by the number of pass in parameter
    for x in range(threads):
        threads = OverviewThread(queue)
        threads.daemon = True
        threads.start()
    for url in fetch_urls:
        queue.put((url))

    # wait for threads finish the tasks
    queue.join()


def get_currency_overview_urls():
    # selenium headless browser
    driver = selenium_driver.get_chrome_driver()
    driver.get(urls.BINANCE_OVERVIEW_URL)
    # web driver waut
    wait = WebDriverWait(driver, 10)
    # wait for page buttons
    page_btn = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "css-b0tuh4")))
    items = page_btn.find_elements(By.XPATH, "//button[contains(@id, 'page')]")

    # get maximum page of the overview to obtain all the currency's info
    last_page = get_maximum_page_overview(items)
    find_currency_overview_test(driver)

    fetch_urls = []

    # Testing
    # for i in range(1, 4):
    #     fetch_urls.append(f"{urls.BINANCE_OVERVIEW_PAGE_URL}?p={i}")

    for i in range(1, last_page + 1):
        fetch_urls.append(f"{urls.BINANCE_OVERVIEW_PAGE_URL}?p={i}")

    driver.close()
    return fetch_urls


def get_maximum_page_overview(items):
    last_page = 0
    if items:
        for item in items:
            largest_page = int(item.text) if item.text.isdigit() else 0
            last_page = largest_page if last_page < largest_page else last_page
    return last_page


# selenium version
def get_currency_data_overview(currency_eles):
    if currency_eles:
        # up down flat
        trend_dict = {"css-li1e6c": "UP", "css-1ez6tx0": "DOWN", "css-ovtrou": "FLAT"}
        for ele in currency_eles:
            # search elements
            name = ele.find_element(By.CLASS_NAME, "css-1x8dg53").text
            price_ele = ele.find_element(By.XPATH, ".//div[@class='css-ydcgk2']/div")
            price = price_ele.text
            # trend assign
            trend = ""
            for k, v in trend_dict.items():
                if price_ele.get_attribute("class") == k:
                    trend = v

            change = ele.find_elements(By.XPATH, ".//div[@class='css-18yakpx']/div")[0].text
            volume = ele.find_element(By.CLASS_NAME, "css-102bt5g").text
            marketcap = ele.find_element(By.CLASS_NAME, "css-s779xv").text

            # append to class global list
            currencies_model.CurrenciesOverview.currency_list.append(
                currencies_model.CurrenciesOverview(
                    name,
                    price,
                    trend,
                    change,
                    volume,
                    marketcap,
                )
            )


def save_currency_overview(df, csv, json):
    if csv:
        # save to csv
        pandas_utils.save_dataframe_to_csv(df, "currency_overview")
    if json:
        # save to json
        pandas_utils.save_dataframe_to_json(df, "currency_overview")


def print_currency_overview_dataframe(df):
    pandas_utils.print_dataframe(df)


def get_sorted_currency_overview_dataframe(sorted_by):
    df = get_currency_overview_dataframe()
    df.sort_values(by=[sorted_by])
    return df


def get_currency_overview_dataframe():
    change_fields = [
        "Name",
        "Price",
        "Trend",
        "Change In 24h",
        "Volume",
        "Market Cap",
    ]
    df = pandas_utils.classlist_to_dataframe(
        currencies_model.CurrenciesOverview.currency_list, currencies_model.CurrenciesOverview.fields, change_fields
    )
    return df


def find_currency_overview_test(driver):
    url = f"{urls.BINANCE_OVERVIEW_PAGE_URL}?p={25}"
    driver.get(url)
    currency_eles = driver.find_elements(By.CLASS_NAME, "css-vlibs4")
    get_currency_data_overview(currency_eles)


# bs4 version
# def find_currencies(driver, currencies_list):
#     for item in currencies_list:
#         # src
#         parsed_item = str(item)
#         c_name = regex_utils.get_item_by_regex(r"href=\"/en/trade/[A-Z]*", parsed_item, "/")
#         c_price = regex_utils.get_item_by_regex(r"\$[^\]]+", parsed_item, "<")
#         c_change = regex_utils.get_item_by_regex(r"(-?[\d\s]+(\.\d+)?%)", parsed_item)
#         c_volume = regex_utils.get_item_by_regex(r"class=\"css-102bt5g\".*\>[^\$][\d,.]+M?", parsed_item, ">")
#         c_marketcap = regex_utils.get_item_by_regex(r"class=\"css-18yakpx\".*\$[\d,.]+?M", parsed_item, ">")
#         # up down flat
#         trend_dict = {"css-li1e6c": "UP", "css-1ez6tx0": "DOWN", "css-ovtrou": "FLAT"}
#         trend_state = ""
#         # not working - initial state on binance is always FLAT
#         for k, v in trend_dict.items():
#             reg_search = re.search(rf"class=\"{k}\"+", parsed_item)
#             if reg_search:
#                 # print(reg_search.group(0))
#                 trend_state = v
#
#             # print(c_marketcap.pop())
#
#         if c_name and c_price and c_change and c_volume and c_marketcap:
#             name = c_name.pop()
#             price = c_price[::-1].pop()
#             volume = c_volume.pop()
#             marketcap = c_marketcap.pop()
#
#             try:
#                 currencies.CurrenciesOverview.currency_list.append(
#                     currencies.CurrenciesOverview(
#                         name,
#                         price,
#                         trend_state,
#                         c_change,
#                         volume,
#                         marketcap,
#                     )
#                 )
#             except IndexError as err:
#                 print(err)
