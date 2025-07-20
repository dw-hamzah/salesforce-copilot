import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.get_customer_detail import get_customer_detail

if __name__ == "__main__":
    print(get_customer_detail("Toko Tani Berkah", "Tajur", "Bogor"))   # search by customer_id
   