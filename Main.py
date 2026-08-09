import pandas as pd
import os

from sheet_loader import sheet_loader
from file_loader import file_loader


def main():
    print(sheet_loader())
    print(file_loader())

if __name__ == "__main__":
    main()
    print("Done")