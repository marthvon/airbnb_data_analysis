#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   airbnb.py - Main Program
#
#   00/00/00: -created
#

from etl import AirbnbETL
from menu import Menu

def main():
    print("Starting Program...")
    if not AirbnbETL.extract("Dataset.csv"):
        return
    
    print("\n\n\t---\tWelcome to the Airbnb Tracker Program\t---\n")
    Menu.start()
    print("\n\n\t---\tExiting Program. Goodbye...\t---\t\n")
    

if __name__ == "__main__":
    main()