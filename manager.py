# Home Depot Manager
# Author : Shaikh Aquib
# Date   : August 2021

import tkinter as tk
import tksheet
import settings
from tkinter import N, S, E, W
from tkinter import filedialog
from layouts.menus.menubar import MenuBar
from processors.sheet_utilities import SheetManipulator
from processors.cache_memory import CacheSaver, CacheRetriever
from processors.data_adapter import DataAdapter


class HomeDepotManager(tk.Tk):

    def __init__(self):
        super().__init__()
        self.cache_file = settings.cache_file
        self.cache = {}

        self.adapter      = DataAdapter()
        self.sheet        = tksheet.Sheet(self, width=800, height=500)
        self.sheet_worker = SheetManipulator(self.sheet, adapter=self.adapter)
        self.csaver       = CacheSaver(self.cache_file)
        self.cretriever   = CacheRetriever(self.cache_file) 
        self.menubar      = MenuBar(self)

        # =============== MENUBAR SETTINGS =================
        self.config(menu=self.menubar)
        # =============== SHEET SETTINGS ===================
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


    def start(self):
        self.mainloop()
