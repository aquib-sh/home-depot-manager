# Sheet Utilities
# Author: Shaikh Aquib
# Data: August 2021

from tkinter import messagebox, filedialog
import pandas
import numpy as np
from layouts.window import InsertRowWindow, InsertWindow

class SheetProcessor:
    """Performs various tasks on sheet.
    
    Parameters
    -----------
    sheet: tksheet.Sheet
        Sheet object on which will be manipulated by utility
    """
    def __init__(self, sheet, adapter):
        self.sheet        = sheet
        self.adapter      = adapter
        self.df           = None
        self.current_file = None
        

    def load_file(self, filename):
        """Loads the file into application by placing it into spreadsheet."""

        if not filename.lower().endswith(".csv"):
            self.df = pandas.read_excel(filename, engine='openpyxl')
        else:
            self.df = pandas.read_csv(filename)

        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)
        self.current_file = filename

    
    def save_file(self):
        """Performs tasks for saving the existing spreadsheet data in CSV and XLSX formats."""
        if self.current_file.lower().endswith(".csv"):
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_csv(self.current_file, index=False)
        
        elif self.current_file.lower().endswith(".xlsx"):
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_excel(self.current_file, index=False)

        else:
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_csv("Output.csv", index=False)
            messagebox.showerror("No name specified","Data sucessfully saved to Output.csv")


    def save_file_as(self, filename):
        """Performs tasks for saving as file for the existing spreadsheet data in CSV and XLSX formats."""
        self.current_file = filename
        self.save_file()


    def insert_new_column(self):
        """Inserts a new column into spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        insert_window = InsertWindow(self.adapter, "new_col", title="Insert Column", size=(400,200), _type="column")
        insert_window.start()
        new_col = self.adapter.get("new_col")
        self.df[new_col] = np.array(["" for i in range(0, len(self.df))])
        # Set the newly inserted data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


    def insert_row(self):
        """Inserts a row into spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        df_cols = self.df.columns.tolist()
        df_dtypes = [self.df[col].dtype for col in self.df]

        insert_window = InsertRowWindow(self.adapter, df_cols, 'Insert Row', size=(400, len(df_cols)*50))
        insert_window.start()

        vals = []
        for row in df_cols:
            vals.append(self.adapter.get(row))
        self.df = self.df.append(pandas.DataFrame([vals], columns=df_cols), ignore_index=True)

        for i in range(0, len(df_cols)):
            self.df[df_cols[i]] = self.df[df_cols[i]].astype(df_dtypes[i])

        df_rows = self.df.to_numpy().tolist()
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


    def delete_column(self):
        """Deletes a column from spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        delete_window = InsertWindow(self.adapter, "del_col", title="Delete Column", size=(400,200), _type="column")
        delete_window.start()
        new_col = self.adapter.get("del_col")
        # Delete Column
        del self.df[new_col]
        # Set the newly modified data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)

    
    def clear_column(self):
        """Clears the value in a column from spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        clear_window = InsertWindow(self.adapter, "clr_col", title="Clear Column", size=(400,200), _type="column")
        clear_window.start()
        new_col = self.adapter.get("clr_col")
        # Clear column
        self.df[new_col] = ['' for i in range(0, len(self.df[new_col]))]
        # Set the newly modified data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


    def get_sheet_dataframe(self) -> pandas.DataFrame:
        """Gets the dataframe from sheet."""
        df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        # return only the data which has values.
        return df[df['SKU'] != '']
