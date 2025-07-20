import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.create_customer import create_customer

if __name__ == "__main__":
    print(create_customer("Toko Langgar Tani,Jl. Kebun Raya No.10,Tajurhalang,Kab Bogor"))
