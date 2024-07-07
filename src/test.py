#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   store.py -
#
#   00/00/00: -created
#

import sys
import time

def print_data(file):
    for line in file:
            for el in line.strip().split(','):
                print(el, end='\t')
            print()

def look_for_UUID(file):
    next(file)
    list_of_id = []
    for line in file:
        el = line.strip().split(',')
        res = el[3] + el[5] + el[6]
        if res:
            list_of_id.append(int(res))
    list_of_id.sort()
    iterator = iter(list_of_id)
    prev = next(iterator)
    try:
        while True:
            curr = next(iterator)
            if prev and prev == curr:
                print(prev)
                prev = None
            else:
                prev = curr
    except:
        pass

def max_and_min(file, index):
    next(file)
    maxnum = None
    minnum = None
    for line in file:
        stream = line.strip().split(',')[index]
        if not stream:
            break
        num = int(float(stream))
        if maxnum is None and minnum is None:
            maxnum = num
            minnum = num
            continue
        if num < minnum: 
            minnum = num
            continue
        if num > maxnum:
            maxnum = num
    print("Maximum: ", maxnum, "\nMinimum: ", minnum)

Host_Response_Rate = 0 # max = 100, min = 0
Host_Identity_Verified = 1 #  max = 1, min = 0
Host_Total_Listings_Count = 2 # max = 749, min = 0
Unique_City_ID = 3 # max = 37, min = 0
Location_Verified = 4 # max = 1, min = 0
Property_Type = 5 # max = 12, min = 0           x axis
Room_Type = 6 # max = 2, min = 0
Max_Accomodation = 7 # max = 16, min = 1
Bathrooms_Count = 8 # max = 6, min = 0
Bedrooms_Count = 9 # max = 5, min = 0          x axis w/ filter as range greater than set
Beds_Count = 10 # max = 16, min = 0
Bed_Type = 11 # max = 4, min = 0
Amenities_Price = 12 # max = 3091, min = 0      y axis
Price = 13 # max = 400000, min = 1000           x and y axis w/ filters as range
Minimum_Nights = 14 # max = 300, min = 1        w/ filters as set
Number_of_Reviews = 15 # max = 404, min = 0
Review_Scores_Rating = 16 # max = 100, min = 20  x axis w/ filters as range
Instant_Bookable = 17 # max = 1, min = 0
Cancellation_Rate = 18 # max = 3, min = 0       y axis w/ filters as range less than set
Reviews_per_Month = 19 # max = 19, min = 0
Fraud_Count = 20 # max = 5, min = 0

def look_for_float(file):
    next(file)
    memory = []
    for line in file:
        temp = line.strip().split(',')
        for index in range(len(temp)):
            if temp[index].find('.') == -1 or index in memory:
                continue
            print(index, "has decimals")
            memory.append(index)

def test_console():
    size = 3
    print("Loading...\t", end='')
    prev = ''
    for i in range(size+1):
        next = str(i) + '/' + str(size)
        print('\b' * len(prev) + next, end='')
        prev = next
        sys.stdout.flush()
        time.sleep(0.3)    
    print("\b\b\b\b\b\b\bSuccessfully")

def test_table():
    header = \
            " Review                |     |         |Max    |      |Cancel| Number of:         | Host                 | Type of:        | Verified    |    |     |Is\n" \
            "-------+-----+---------|Price|Amenities|Accom- |Min   |lation|-------+---+--------+-------------+--------+--------+----+---+----+--------|City|Fraud|Instant\n" \
            "Ratings|Count|per Month|     |  Price  |odation|Nights| Rate |Bedroom|Bed|Bathroom|Response Rate|Listings|Property|Room|Bed|Host|Location| ID |Count|Booking\n" 
    grd="-------+-----+---------+-----+---------+-------+------+------+-------+---+--------+-------------+--------+--------+----+---+----+--------+----+-----+-------\n"
    spaces = [7,5,9,5,9,7,6,6,7,3,8,13,8,8,4,3,4,8,4,5,7]
    print(header + grd, end='')
    for i in spaces[:-1:]:
        print(' ' * i + '|', end='')
    print(' ' * spaces[-1])

def main():
    try:
        with open("Dataset.csv", 'r') as file:
            #print_data(file)
            #look_for_UUID(file)
            max_and_min(file, 20)
            #look_for_float(file)
            #test_console()
            #test_table()
            pass
    except:
        print("file not found")

if __name__ == "__main__":
    main()

