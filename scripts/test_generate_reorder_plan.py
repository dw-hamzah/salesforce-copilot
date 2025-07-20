import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.generate_reorder_plan import generate_reorder_plan

if __name__ == "__main__":
    df = generate_reorder_plan()
    print(df)