import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.take_order import take_order

if __name__ == "__main__":
    print(take_order("Sembada, order: Benih Cabai Besar - 5, Amora - 8"))
