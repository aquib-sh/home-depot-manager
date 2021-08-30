# Home Depot Manager
# Author : Shaikh Aquib (shaikhaquib394@gmail.com)
# Date   : August 2021

import threading
import tkinter as tk
import tksheet
import settings
from tkinter import N, S, E, W
from tkinter import filedialog
from layouts.menus.menubar import MenuBar
from layouts.window import ScanPriceWindow
from processors.sheet_utilities import SheetProcessor
from processors.cache_memory import CacheSaver, CacheRetriever
from processors.data_adapter import DataAdapter
from services.client import HomeDepotClient


class HomeDepotManager(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Home Depot Manager")
        self.cache_file = settings.cache_file
        self.cache = {}

        self.raw_df = None

        self.client       = HomeDepotClient()
        self.adapter      = DataAdapter()
        self.sheet        = tksheet.Sheet(self, width=800, height=500, total_rows=1000, total_columns=4)
        self.sheet_worker = SheetProcessor(self.sheet, adapter=self.adapter)
        self.csaver       = CacheSaver(self.cache_file)
        self.cretriever   = CacheRetriever(self.cache_file) 
        self.menubar      = MenuBar(self)

        # Columns
        self.store_no_col = settings.sheet_columns[0]
        self.sku_col      = settings.sheet_columns[1]
        self.price_col    = settings.sheet_columns[3]

        # =============== MENUBAR SETTINGS =================
        self.config(menu=self.menubar)
        # =============== SHEET SETTINGS ===================
        self.sheet.headers(settings.sheet_columns)
        self.sheet.enable_bindings(("all"))
        self.sheet.grid(row=1, column=0, sticky=N+S+E+W)
        self.sheet.grid_columnconfigure(1, weight=3)
        self.sheet.grid_rowconfigure(1, weight=3)
        # ===================================================
        # Make display flexible in size
        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=3)


    def open_file(self):
        """Opens up file chooser to select the file
           calls load_file() to import data into spreadsheet.
        """
        start_dir = "/"
        if self.cretriever.cache_exists():
            self.cache = self.cretriever.retrieve_cache()
            if "recently_opened" in self.cache: 
                start_dir = self.cache["recently_opened"]

        filename = filedialog.askopenfilename(initialdir=start_dir,
                                        title="Open a file",
                                        filetypes=(
                                            ("csv files", "*.csv"), 
                                            ("xlsx files", "*.xlsx"),
                                            ("all files", "*.*")
                                        )
                                    )
        if filename == '' : return
        self.sheet_worker.load_file(filename)
        self.csaver.save_cache(self.cache)


    def save_file_as(self):
        file_name = filedialog.asksaveasfilename(initialdir="/",
                                title="Choose file",
                                filetypes=(
                                            ("csv files", "*.csv"), 
                                            ("xlsx files", "*.xlsx"),
                                            ("all files", "*.*")
                                        )
                                    )
        if file_name == '' : return
        if (not file_name.endswith(".csv")) and (not file_name.endswith(".xlsx")):
            file_name += ".csv"
        self.sheet_worker.save_file_as(file_name)


    def __scan_and_update_price(self):
        """Scans for the pricing and updates the sheet by price values."""
        raw_df = self.sheet_worker.get_sheet_dataframe()
        df = raw_df[raw_df['SKU']!='']
        #prev = ""
        for i in range(0, len(df[self.sku_col])):
            row = df.iloc[i]
            #store_no = str(row[self.store_no_col])
            sku = str(row[self.sku_col])
            print(f"[+] Searching for product: {sku}")
            self.client.bot.move(f'https://homedepot.com/s/{sku}')
            price = self.client.get_price()
            raw_df.loc[i][self.price_col] = price
            # prev = store_no
        self.raw_df = raw_df


    def scan_and_update_price(self):
        t = threading.Thread(target=self.__scan_and_update_price)
        t.start()
        t.join()
        self.sheet_worker.update_sheet(self.raw_df)
        print("[+] Sheet updated with latest data")


    def start_scan_process(self):
        scan_window = ScanPriceWindow()
        scan_window.start()


    def start(self):
        self.mainloop()


if __name__ == "__main__":
    manager = HomeDepotManager()
    manager.start()
    manager.client.bot.shutdown()