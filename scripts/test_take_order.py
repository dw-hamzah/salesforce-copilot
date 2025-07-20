import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.take_order import take_order

if __name__ == "__main__":
    print(take_order("Toko Tani Berkah, order: Benih Jagung Nogorojo - 10, Benih Cabai Besar Aleron F1 - 15, Emasol 30E - 8"))
