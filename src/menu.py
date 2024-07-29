#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   menu.py - 
#
#   00/00/00: -created
#

from etl import AirbnbETL

import numpy

def _prompt_realt(prompt : str, scope = None) -> float:
    while True:
        try:
            if scope is None:
                return float(input(prompt))
            res = float(input(prompt))
            if res < scope[0]:
                print("[Alert]: Entered value is below the available range of values. Re-enter")
                continue
            if res > scope[1]:
                print("[Alert]: Entered value is above the available range of values. Re-enter")
                continue
            return res
        except:
            print("[Error]: Invalid input has non numeric characters. Re-enter.")

def _prompt_enum(max : int, prompt : str) -> int:
    while True:
        try:
            res = int(input(prompt))
            if res < 0 or res > max:
                print("[Alert]: Invalid input is not within range. Re-enter.")
                continue
            return res
        except:
            print("[Error]: Invalid input has non numeric characters. Re-enter.")

class _FilterMenu:
    def _option_bedroom_counts():
        limits = (AirbnbETL.bedroom_count_index.get_min(), AirbnbETL.bedroom_count_index.get_max())
        print("Available Bedroom Range from", limits[0], "to", limits[1])
        value = _prompt_realt("\tEnter the least number of bedrooms required: ", limits)
        AirbnbETL.transform(AirbnbETL.bedroom_count_index, value)

    def _option_price():
        limits = (AirbnbETL.price_index.get_min(), AirbnbETL.price_index.get_max())
        print("Available Price Range from", limits[0], "to", limits[1])
        mins = _prompt_realt("\tEnter Minimum range for price: ", limits)
        maxs = _prompt_realt("\tEnter Maximum range for price: ", limits)
        AirbnbETL.transform(AirbnbETL.price_index, mins, maxs)

    def _option_minimum_nights():
        limits = (AirbnbETL.minimum_nights_index.get_min(), AirbnbETL.minimum_nights_index.get_max())
        print("Available Minimum Nights Range from", limits[0], "to", limits[1])
        value = _prompt_realt("\tEnter set number of minimum nights required: ", limits)
        AirbnbETL.transform(AirbnbETL.minimum_nights_index, value)

    def _option_review_score_rating():
        limits = (AirbnbETL.review_scores_rating_index.get_min(), AirbnbETL.review_scores_rating_index.get_max())
        print("Available Review Score Rating Range from", limits[0], "to", limits[1])
        mins = _prompt_realt("\tEnter Minimum range for the review score rating: ", limits)
        maxs = _prompt_realt("\tEnter Maximum range for the review score rating: ", limits)
        AirbnbETL.transform(AirbnbETL.review_scores_rating_index, mins, maxs)

    def _option_cancellation_rate():
        limits = (AirbnbETL.cancellation_rate_index.get_min(), AirbnbETL.cancellation_rate_index.get_max())
        print("Available Cancellation Rate Range from", limits[0], "to", limits[1])
        value = _prompt_realt("\tEnter the atmost number of cancellation rate required: ", limits)
        AirbnbETL.transform(AirbnbETL.cancellation_rate_index, value)

    option = numpy.array([
        _option_bedroom_counts,
        _option_price,
        _option_minimum_nights,
        _option_review_score_rating,
        _option_cancellation_rate
    ])

class Menu: 
    _graph_case = numpy.array([
        AirbnbETL.price_index, 
        AirbnbETL.bedroom_count_index,
        AirbnbETL.property_type_index,
        AirbnbETL.review_scores_rating_index,
    ])


    def _option_add_filter():
        while True:
            mode = _prompt_enum(6,
                "\nSelect a FILTER to apply:" \
                "\n\t(1) Bedroom Counts" \
                "\n\t(2) Price" \
                "\n\t(3) Minimum Nights" \
                "\n\t(4) Review Score Rating" \
                "\n\t(5) Cancellation Rate" \
                "\n\t(6) Go Back\n" \
                "\nPick and option on how to handle the data [1~6]: "
            )-1
            if mode == 5:
                return
            _FilterMenu.option[mode]()

    def _option_graph_data():
        x = _prompt_enum(4,
            "\nATTRIBUTES:" \
            "\n\t(1) Price" \
            "\n\t(2) Bedroom Count" \
            "\n\t(3) Property Type" \
            "\n\t(4) Review Score Rating" \
            "\nSelect attribute to bind to the X-axis [1~4]: "
        )-1
        AirbnbETL.load_graph(Menu._graph_case[x])


    _menu_option = numpy.array([
        _option_add_filter,
        lambda: AirbnbETL.load_table(),
        _option_graph_data,
        lambda: AirbnbETL.reset_filters()
    ])


    def start():
        while True:
            mode : int = _prompt_enum(5,
                "\nMENU OPTIONS:" \
                "\n\t(1) Add Filters" \
                "\n\t(2) Print Names" \
                "\n\t(3) Graph Data" \
                "\n\t(4) Reset Filters" \
                "\n\t(5) Exit\n" \
                "\nPick an option on how to handle the data [1~5]: "
            )-1
            if mode == 4:
                return
            Menu._menu_option[mode]()

