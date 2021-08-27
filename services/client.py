import sys
sys.path.append("../")

import time
import settings
from bot import BotMaker
from services.store_finder import StoreFinder
from services.json_helper import JSONHelper

class HomeDepotClient:

    def __init__(self) -> None:
        self.bot = BotMaker(behead=settings.headless, browser=settings.browser)
        self.bot.move(settings.website)
        self.locater = StoreFinder(self.bot)
        self.helper  = JSONHelper()
        self.xpaths = self.helper.get_json_data(settings.xpaths_file)

    def search_by_sku(self, sku: str) -> None:
        """Searches for the product by the SKU param."""
        self.bot.get_element(self.xpaths['search_box']).clear()
        self.bot.get_element(self.xpaths['search_box']).send_keys(sku)
        self.bot.get_element(self.xpaths['search_btn']).click()
        
    def get_price(self) -> str:
        """Returns the product price present on current page."""
        time.sleep(2)
        price_elems = self.bot.get_elements(self.xpaths['price_elems'])
        return str(price_elems[0].text + price_elems[1].text)
