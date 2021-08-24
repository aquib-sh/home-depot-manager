import sys
sys.path.append("../")

from manager import HomeDepotManager

manager = HomeDepotManager()
manager.load_file('sample.xlsx')
manager.start()