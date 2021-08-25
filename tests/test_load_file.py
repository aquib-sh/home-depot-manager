import sys
sys.path.append("../")

from manager import HomeDepotManager

manager = HomeDepotManager()
manager.sheet_worker.load_file('sample.xlsx')
manager.start()