#Author : Shaikh Aquib
#Date : June 2021

import time
import sys
import threading
import tkinter as tk
from datetime import datetime
from tkinter import Scrollbar, ttk
from tkinter import messagebox
from tkinter.constants import BOTTOM, CENTER, E, HORIZONTAL, LEFT, END, RIGHT, W, Y
sys.path.append('../')
from tkinter import Label, Button, Text


class Application(tk.Tk):
    """A class for main window of the application.

    This class serves as main tkinter window which can contain menus, submenus, charts, etc.

    Methods
    -------

    """
    def __init__(self, title:str, size:tuple):
        """
        Parameters
        ----------
        title : str
            Title of the window

        size : tuple
            Size of window (x:int, y:int) where x is width and y is height.
        """
        super().__init__()
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.title(title)
        self.pack_propagate(0)


    def start(self):
        """Displays the window by starting the mainloop."""
        self.mainloop()

    def exit_window(self):
        self.destroy()



class TopLevelWindow(tk.Toplevel):
    """A class for top level window of the application.

    This class serves as main tkinter window which can contain menus, submenus, charts, etc.

    Methods
    -------
    """
    def __init__(self, title: str, size: tuple):
        """
        Parameters
        ----------
        title : str
            Title of the window

        size : tuple
            Size of window (x:int, y:int) where x is width and y is height.
        """
        super().__init__()
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.title(title)

    def start(self):
        """Displays the window by starting the mainloop."""
        self.mainloop()

    def exit_window(self):
        self.quit()
        self.destroy()



class InsertWindow(TopLevelWindow):
    """Insert window which inserts column and rows to the spreadsheet.

    Parameters
    ----------
    adapter : chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    _key : str
        Key for the return value of textbox.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.

    _type : str
        Type of window (column or row)
    """
    def __init__(self, adapter, _key, title:str, size:tuple, _type:str):
        super(InsertWindow, self).__init__(title=title, size=size)

        # If _type is not column or row then raise exception
        if _type.lower() not in ["column", "row"]:
            raise Exception(f"Invalid Type:\n_type={_type}\nType must be _type=column or _type=row")

        self.adapter = adapter
        self.adapter_key = _key

        label = Label(self, text=f"{_type.capitalize()} Name:")
        self.text_box = ttk.Entry(self)
        self.insert_btn = Button(self, text="Apply", command=self.transfer_value_and_destroy)

        label.pack()
        Label(self, text="").pack() #empty space
        self.text_box.pack()
        Label(self, text="").pack() #empty space
        self.insert_btn.pack()


    def transfer_value_and_destroy(self) -> str:
        """Returns the textbox value."""
        self.adapter.insert(self.adapter_key, self.text_box.get())
        self.exit_window()



class InsertRowWindow(TopLevelWindow):
    """Insert window which inserts rows to the spreadsheet.

    Parameters
    ----------
    adapter : chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    columns : list
        columns of the current dataframe, adapter values will also be returned with these names.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.

    """
    def __init__(self, adapter, columns: list, title: str, size: tuple):
        super(InsertRowWindow, self).__init__(title=title, size=size)

        self.adapter = adapter
        self.columns = columns
        self.register = {}

        r=0 # row index
        for col in self.columns:
            Label(self, text=f"{col} : ").grid(row=r, column=0)
            entry = ttk.Entry(self)
            self.register[col] = entry
            entry.grid(row=r, column=1)
            # Register the entry boxes to retrieve further by col names.
            r += 1

        self.insert_btn = Button(self, text="Apply", command=self.transfer_value_and_destroy)
        self.insert_btn.grid(row=r, column=0, padx=(150, 0), pady=(100, 100))


    def transfer_value_and_destroy(self) -> str:
        """Returns the textbox value."""
        for col in self.columns:
            self.adapter.insert(col, self.register[col].get())
        self.exit_window()



class DeleteWindow(TopLevelWindow):
    """Insert window which inserts column and rows to the spreadsheet.

    Parameters
    ----------
    adapter : chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    _key : str
        Key for the return value of dropdown.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.

    _type : str
        Type of window (column or row)
    """
    def __init__(self, adapter, _key, title:str, size:tuple, _type:str):
        super(DeleteWindow, self).__init__(title=title, size=size)

        # If _type is not column or row then raise exception
        if _type.lower() not in ["column", "row"]:
            raise Exception(f"Invalid Type:\n_type={_type}\nType must be _type=column or _type=row")

        self.adapter = adapter
        self.adapter_key = _key

        self.label = Label(self, text=f"{_type.capitalize()}:")
        self.n = tk.StringVar()
        self.choice = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n)
        self.del_btn = Button(self, text="Delete", command=self.transfer_value_and_destroy)

        # Attach widgets to window using grid layout
        self.label.grid(row=0, column=0)
        self.choice.grid(row=1, column=0)
        self.del_btn.grid(row=2, column=0, padx=(100,100))


    def update_dropdown(self, values):
        self.choice['values'] = values
        self.choice.current(0)


    def transfer_value_and_destroy(self):
        """Returns the textbox value."""
        self.adapter.insert(self.adapter_key, self.choice.get())
        self.exit_window()



class OptionsWindow(TopLevelWindow):
    """Takes input settings for building CutChart view.
    
    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    title: str (default="Chartify Options")
        Title for window.

    size: tuple (default=(400, 400))
        Size of the window.
    """
    def __init__(self, adapter, size=(800,600), title="Options"):
        super(OptionsWindow, self).__init__(title=title, size=size)
        self.adapter = adapter
        # =================================== LEFT SIDE ===================================================
        ttk.Label(self, text="Table Font:")                .grid(row=0, column=0, sticky='W', pady=(0, 50))
        ttk.Label(self, text="Table Font Size:")           .grid(row=1, column=0, sticky='W', pady=(0, 50))

        self.n1 = tk.StringVar()
        self.n2 = tk.StringVar()

        self.table_font      = ttk.Combobox(self, state="readonly", textvariable=self.n1)
        self.table_fsize     = ttk.Combobox(self, state="readonly", textvariable=self.n2)

        self.table_font     .grid(row=0, column=1, sticky='E', pady=(0, 50))
        self.table_fsize    .grid(row=1, column=1, sticky='E', pady=(0, 50))
        #=======================================================================================================
        self.table_fsize['values'] = list(i for i in range(10, 30))

        apply_btn          = ttk.Button(self, text="Apply", command=self.transfer_value_and_destroy)
        close_btn          = ttk.Button(self, text="Close", command=self.destroy_window)

        apply_btn         .grid(row=6, column=0, padx=(100, 50), pady=(100,0))
        close_btn         .grid(row=6, column=2, padx=(50, 0), pady=(100,0))
        self.protocol("WM_DELETE_WINDOW", self.destroy_window)

    def add_fonts(self, fonts: list):
        self.table_font['values'] = fonts

    def transfer_value_and_destroy(self):
        """Inserts the textbox value into the adapter."""
        self.adapter.insert("table-font",               self.table_font.get())
        self.adapter.insert("table-font-size" ,         self.table_fsize.get)
        self.exit_window()


    def destroy_window(self) -> None:        
        self.adapter.insert("table-font",      None)
        self.adapter.insert("table-font-size", None)
        self.exit_window()


class ScanPriceWindow(TopLevelWindow):
    """Takes input settings for building CutChart view.
    
    Parameters
    ----------
    title: str (default="Chartify Options")
        Title for window.

    size: tuple (default=(400, 400))
        Size of the window.
    """
    def __init__(self, size=(400,200), title="Scan and Update Prices"):
        super(ScanPriceWindow, self).__init__(title=title, size=size)
        self.start_btn = Button(self, text="Start Scan", command=self.start_scan)
        self.start_btn.pack()

    def start_scan(self):
        """Starts the scanning process and updates the sheet with latest price data."""
        status = Label(self, fg='red', font=("Arial", 15))
        status.pack(pady=50)
        status.config(text='Scanning for prices...\n\nDo not close this window!', fg='red')
        self.update()

        # t = threading.Thread(target=self.master.scan_and_update_price)
        # t.start()
        # t.join()
        self.master.scan_and_update_price()
        
        status.config(text='Scan Completed!\n\nNow, You can close this window!', fg='green')
    
    def start(self):
        super().start()