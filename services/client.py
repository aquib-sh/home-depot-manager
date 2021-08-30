import sys
sys.path.append("../")

import time
import settings
from bot import BotMaker
from services.store_finder import StoreFinder
from services.json_helper import JSONHelper
from selenium.common.exceptions import StaleElementReferenceException


class HomeDepotClient:

    def __init__(self) -> None:
        self.bot = BotMaker(behead=settings.headless, browser=settings.browser)
        self.bot.move(settings.website)
        self.locater = StoreFinder(self.bot)
        self.helper  = JSONHelper()
        self.xpaths = self.helper.get_json_data(settings.xpaths_file)

    def search_by_sku(self, sku: str) -> None:
        """Searches for the product by the SKU param."""
        while True:
            try:
                self.bot.get_element(self.xpaths['search_box']).clear()
                break
            except StaleElementReferenceException:
                self.bot.get_element(self.xpaths['search_box']).clear()
            print("entry 1")
        while True:
            try:
                self.bot.get_element(self.xpaths['search_box']).send_keys(sku)
                break
            except StaleElementReferenceException:
                self.bot.get_element(self.xpaths['search_box']).send_keys(sku)
                print("entry 2")
        while True:
            try:
                self.bot.get_element(self.xpaths['search_btn']).click()
                break
            except StaleElementReferenceException:
                self.bot.get_element(self.xpaths['search_btn']).click()
            print("entry 3")

    def get_price(self) -> str:
        """Returns the product price present on current page."""
        time.sleep(2)
        price_elems = self.bot.get_elements(self.xpaths['price_elems'])
        price = str(price_elems[0].text + price_elems[1].text)

        if len(price_elems) == 3:
            price_elems = self.bot.get_elements(self.xpaths['price_elems'])
            price = str(price_elems[0].text + price_elems[1].text + "."+price_elems[2].text)
        
        return price

    def select_store_by_number(self, store_number: str) -> None:
        """Selects the store using StoreFinder."""
        self.locater.select_store_by_number(store_number)