import os

website          = "https://www.homedepot.com/"
store_search_url = "https://www.homedepot.com/l/" 
browser          = "Firefox"
headless         = True
cache_file       = "app_data.json"
xpaths_file      = os.path.abspath(os.path.join("services", "xpaths.json"))
sheet_columns    = ['Store #', 'SKU', 'Item Description', 'Current Price']