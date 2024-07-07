#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   etl.py - 
#
#   00/00/00: -created
#

from store import AirbnbStore
from console import Console
from query import *

import numpy
import matplotlib.pyplot as plt 

def _next_or_null(iter):
    try:
        return next(iter)
    except StopIteration:
        return None

class _Graph:
    def __init__(self):
        self._xAxis = []
        self._yAxis = []
        self._yTotal = 0
        self._index = 0

    def add(self, val):
        if val is None:
            return
        self._yTotal += val
        self._index += 1

    def push(self, xAxis):
        self._xAxis.append(xAxis)
        self._yAxis.append(self._yTotal / self._index)
        self._yTotal = 0
        self._index = 0

    def display(self, grid_position, query, ylabel, *args):
        plt.subplot(grid_position)
        plt.xlabel(query.label)
        plt.ylabel(ylabel)
        query.graph_callback(self._xAxis, self._yAxis, *args)

class AirbnbETL:
    _data = None
    _filtered_data = None
    _filter_history = []

    # x-y-axis for graph
    price_index = RangeQuery("Price", lambda *args: plt.plot(*args))
    # x-axis for graph
    bedroom_count_index = GreaterThanQuery("Bedroom Count", lambda *args: plt.bar(*args))
    property_type_index = Query("Property Type", lambda *args: plt.bar(*args)) 
    review_scores_rating_index = RangeQuery("Review Score Rating", lambda *args: plt.plot(*args))
    # y-axis for graph
    cancellation_rate_index = LessThanQuery()
    # others
    minimum_nights_index = FindQuery()

    def extract(filename, is_log = True):
        console = Console(is_log)
        if AirbnbETL._data is not None:
            console.log("[Error]: Data already exists\n\t'AirbnbETL.extract' has already been called once.\n\tAny further calls to 'AirbnbETL.extract' will be discarded")
            return False
        
        temp = []
        console.log("Opening file \"", filename, "\"...")
        try:
            with open(filename, 'r') as file:
                console.success()

                console.log("Extracting data from file...")
                next(file) # skip headers
                console.success()

                console.log_loading("Initializing buffer...")
                index = 0
                for line in file:
                    if not line:
                        continue
                    temp_store = AirbnbStore(*line.strip().split(','))
                    temp.append(temp_store)
                    AirbnbETL.price_index.push_to_buffer(index, temp_store.price)
                    AirbnbETL.bedroom_count_index.push_to_buffer(index, temp_store.bedroom_count)
                    AirbnbETL.property_type_index.push_to_buffer(index, temp_store.property_type)
                    AirbnbETL.review_scores_rating_index.push_to_buffer(index, temp_store.review_scores_rating)
                    AirbnbETL.cancellation_rate_index.push_to_buffer(index, temp_store.cancellation_rate)
                    AirbnbETL.minimum_nights_index.push_to_buffer(index, temp_store.minimum_nights)
                    console.increment()
                    index += 1
                console.success()

            console.log("Initializing In-Memory Database...")
            AirbnbETL._data = numpy.array(temp, dtype=AirbnbStore)
            console.success()


            console.log_loading_size_of(6, "Initializing query for indexed attributes...")

            AirbnbETL.price_index.init()
            console.increment()
            AirbnbETL.bedroom_count_index.init()
            console.increment()
            AirbnbETL.property_type_index.init()
            console.increment()
            AirbnbETL.review_scores_rating_index.init()
            console.increment()
            AirbnbETL.cancellation_rate_index.init()
            console.increment()
            AirbnbETL.minimum_nights_index.init()
            console.increment()
            console.success()

            console.log("Finished...")
            return True
        except FileNotFoundError:
            console.fail()
            print("[Error]: File not found...\tExiting Program")
            return False

                     
    def transform(query_attribute, *args, is_log=True):
        debug_console = Console(is_log)
        if AirbnbETL._filtered_data is None:
            debug_console.log("Appplying the first filter on data...")
            AirbnbETL._filtered_data = query_attribute.filter(*args)
            # _filter_history data type: [[ array-like of indexes of a combination of filter, indexed attribute applied to the array-like], ]
            AirbnbETL._filter_history.append([None, query_attribute]) 
            debug_console.success()
            return
        for index in range(len(AirbnbETL._filter_history)):
            if AirbnbETL._filter_history[index][1] is not query_attribute:
                continue
            debug_console.log("Filter of this type has already been applied.\n\tDiscarding previously applied filter of this type...")
            query_attribute.filter(*args)

            i = index
            if i == 0:
                AirbnbETL._filter_history[0] =[query_attribute, query_attribute]
                i = 1
            else:
                AirbnbETL._filter_history[i][1] = query_attribute
            debug_console.success()

            debug_console.log_loading_size_of(len(AirbnbETL._filter_history) - i, "Re-appplying all other filters...")
            for (el, j) in zip(AirbnbETL._filter_history[i-1:-1:], range(i, len(AirbnbETL._filter_history))):
                AirbnbETL._filter_history[j][0] = AirbnbETL._filter_history[j][1].combine_filter(el[0])
                debug_console.increment()
            AirbnbETL._filtered_data = AirbnbETL._filter_history[-1][0]
            debug_console.success()
            return
        debug_console.log("Combining new filter with previously filtered data...")
        AirbnbETL._filter_history[-1][0] = AirbnbETL._filtered_data
        AirbnbETL._filter_history.append([None, query_attribute]) 
        AirbnbETL._filtered_data = query_attribute.filter(*args).combine_filter(AirbnbETL._filtered_data)
        debug_console.success()

    def reset_filters():
        for attribute in AirbnbETL._filter_history:
            attribute[1].clear()
        AirbnbETL._filtered_data = None
        AirbnbETL._filter_history = []
        print("Filters has been reset...\tSuccessfully")
    

    _grd=[[" Review              |        |", "         |Max    |      |Cancel", "| Number of:         | Host                | Type of:        | Verified    |", "    |     |Is\n"],
          ["------+-----+--------| Price  |", "Amenities|Accom- |Min   |lation", "|-------+---+--------+------------+--------+--------+----+---+----+--------|", "City|Fraud|Instant\n"],
          ["Rating|Count|perMonth|        |", "  Price  |odation|Nights| Rate ", "|Bedroom|Bed|Bathroom|ResponseRate|Listings|Property|Room|Bed|Host|Location|", " ID |Count|Booking\n"], 
          ["------+-----+--------+--------+", "---------+-------+------+------", "+-------+---+--------+------------+--------+--------+----+---+----+--------+", "----+-----+-------\n"]
    ]
    _spaces = [6,5,8,8,9,7,6,6,7,3,8,12,8,8,4,3,4,8,4,5,7]
    def load_table():
        # printing table header on top
        for gr in AirbnbETL._grd:
            for g in gr: 
                print(g, end='')
        # printing data
        if AirbnbETL._filtered_data is not None:
            for i in AirbnbETL._filtered_data:
                AirbnbETL._data[int(i)].print_onTable(AirbnbETL._spaces)
        else:
            for el in AirbnbETL._data:
                el.print_onTable(AirbnbETL._spaces)
        # printing table header on the bottom
        for g in AirbnbETL._grd[-1]:
            print(g, end='')
        for oddcol, evencol in zip(AirbnbETL._grd[-2::-1], AirbnbETL._grd[:-1:]): # flip all odd columns and keep even columns as the same
            for o, e in zip(oddcol[::2], evencol[1::2]):
                print(o + e, end='')

    def load_names():
        if AirbnbETL._filtered_data is not None:
            for i in AirbnbETL._filtered_data:
                print(AirbnbETL._data[int(i)])
        else:
            for el in AirbnbETL._data:
                print(el)


    def load_graph(query_attribute, is_log=True):
        debug_console = Console(is_log)
        
        debug_console.log("Arranging data based on attribute assigned on the X-Axis...")
        ordered_data = query_attribute.order_data(AirbnbETL._filtered_data) if AirbnbETL._filtered_data is not None else query_attribute
        debug_console.success()

        price_graph = _Graph()
        amenities_graph = _Graph()
        cancellation_graph = _Graph()
        
        debug_console.log_loading("Retrieving values for the Y-Axis...")
        qElptr = iter(ordered_data)
        qEl = _next_or_null(qElptr)
        while qEl is not None:
            prev_x = qEl.value
            store = AirbnbETL._data[int(qEl)]
            price_graph.add(store.price)
            amenities_graph.add(store.amenities_price)
            cancellation_graph.add(store.cancellation_rate)
            qEl = _next_or_null(qElptr)
            if qEl is not None and qEl.value == prev_x:
                continue
            price_graph.push(prev_x)
            amenities_graph.push(prev_x)
            cancellation_graph.push(prev_x)
            debug_console.increment()
        debug_console.success()

        print("Showing Graph...", end='')
        plt.figure(1)
        if query_attribute is not AirbnbETL.price_index:
            price_graph.display(311, query_attribute, "Price")
        amenities_graph.display(312, query_attribute, "Amenities Price")
        cancellation_graph.display(313, query_attribute, "Cancellation Rate")
        plt.show()
        print("Closed")


    def get_data_size():
        return len(AirbnbETL._data)

