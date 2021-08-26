#Author : Shaikh Aquib
#Date : June 2021

import tkinter as tk


class MenuBar(tk.Menu):
    """ MenuBar

    MenuBar containing other menus and submenus
    """
    def __init__(self, master:tk.Tk):
        """
        Parameters
        ----------
        master : tk.Tk
            Parent window where menu is to be displayed.
        
        label  : str 
            Label of the current menubar
        """
        super().__init__(master)
        self.master = master

        # Add the first 3 menus
        filemenu  = tk.Menu(self, tearoff=0)
        editmenu  = tk.Menu(self, tearoff=0)
        chartmenu = tk.Menu(self, tearoff=0)
        toolsmenu = tk.Menu(self, tearoff=0)

        # Give names to above menus
        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Edit", menu=editmenu)
        self.add_cascade(label="3D Chart", menu=chartmenu)
        self.add_cascade(label="Tools", menu=toolsmenu)

        # SubMenu inside editmenu
        insertmenu = tk.Menu(editmenu, tearoff=0)
        deletemenu = tk.Menu(editmenu, tearoff=0)
        clearmenu  = tk.Menu(editmenu, tearoff=0)

        # Add labels to the above submenus inside edit menu
        editmenu.add_cascade(label="Insert", menu=insertmenu)
        editmenu.add_cascade(label="Delete", menu=deletemenu)
        editmenu.add_cascade(label="Clear", menu=clearmenu)

        # Row, column options for insert, delete and clear
        insertmenu.add_command(label="Row", command=None)
        insertmenu.add_command(label="Column", command=self.master.sheet_worker.insert_new_column)
        
        deletemenu.add_command(label="Row", command=None)
        deletemenu.add_command(label="Column", command=self.master.sheet_worker.delete_column)

        #clearmenu.add_command(label="Row", command=None)
        clearmenu.add_command(label="Column", command=self.master.sheet_worker.clear_column)

        filemenu.add_command(label="Open", command=self.master.open_file)
        filemenu.add_command(label="Save", command=self.master.sheet_worker.save_file)
        filemenu.add_command(label="Save as", command=self.master.save_file_as)
        
