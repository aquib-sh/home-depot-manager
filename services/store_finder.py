# StoreFinder
# Author : Shaikh Aquib
# Date   : August 2021

import sys
sys.path.append("../")

import time
import settings
from services.json_helper import JSONHelper


class StoreFinder:
    """Finds the HomeDepot store by store number or zip code."""

    def __init__(self, bot) -> None:
        """
        bot: bot.BotMaker
            BotMaker object with home depot page loaded.
        """
        self.bot = bot
        self.helper  = JSONHelper()
        self.xpaths = self.helper.get_json_data(settings.xpaths_file)


    def select_store_by_number(self, store_number: str):
        """Selects store based on number."""
        self.bot.move(settings.store_search_url)
        self.bot.get_element(self.xpaths["store_search_box"]).clear()
        self.bot.get_element(self.xpaths["store_search_box"]).send_keys(store_number)
        self.bot.get_element(self.xpaths["store_search_btn"]).click()
        time.sleep(2)

        # Search all store elements if #store_number is found 
        # then click the shop the store element
        stores = self.bot.get_elements(self.xpaths["store_list_section_elems"])
        for i in range(0, len(stores)):
            desired_store = False
            store = stores[i]
            while True:
                try:
                    desired_store = '#'+str(store_number) in store.text
                    break
                except:
                    stores = self.bot.get_elements(self.xpaths["store_list_section_elems"])
                    store = stores[i]

            if desired_store:
                self.bot.get_element(self.xpaths["shop_store_btn" ], 
                        elem=store).click()
                print(f"[+] Selected #{store_number} store.")

