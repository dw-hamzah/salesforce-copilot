import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.get_last_transaction import get_last_transaction

if __name__ == "__main__":
    print(get_last_transaction("1"))   # search by customer_id
    print(get_last_transaction("Tani Berkah"))  # search by partial customer name