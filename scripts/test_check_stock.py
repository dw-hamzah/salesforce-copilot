import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.check_stock import check_stock

if __name__ == "__main__":
    print(check_stock("1"))  # test by product_id
    print(check_stock("2"))  
    print(check_stock("3"))  
    print(check_stock("4"))  
    print(check_stock("5"))  
    print(check_stock("6"))  
    print(check_stock("7"))  
    print(check_stock("8"))  
    # print(check_stock("redzone"))  # test by partial product name