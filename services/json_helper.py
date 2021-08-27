# JSON Helper
# Author : Shaikh Aquib
# Data   : August 2021

import os
import json

class JSONHelper:
    def get_json_data(self, filename):
        if not os.path.exists(filename):
            print(f"[!] {filename} does not exist")
            return None
        
        else:
            if not filename.endswith(".json"):
                print(f"[!] {filename} is not a JSON file")
                return None

            else:
                fp = open(filename, 'r') 
                return json.load(fp)

