#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   store.py -
#
#   00/00/00: -created
#


class AirbnbStore:
    def __init__(self, *args):
        self.host_response_rate = int(args[0]) if args[0] else None
        self.host_identity_verified = bool(args[1]) if args[1] else None
        self.host_total_listings_count = int(args[2]) if args[2] else None
        self.unique_city_id = int(args[3]) if args[3] else None
        self.location_verified = bool(args[4]) if args[4] else None
        self.property_type = int(args[5]) if args[5] else None
        self.room_type = int(args[6]) if args[6] else None
        self.max_accomodation = int(args[7]) if args[7] else None
        self.bathroom_count = float(args[8]) if args[8] else None
        self.bedroom_count = int(args[9]) if args[9] else None
        self.beds_count = int(args[10]) if args[10] else None
        self.bed_type = int(args[11]) if args[11] else None
        self.amenities_price = float(args[12]) if args[12] else None
        self.price = float(args[13]) if args[13] else None
        self.minimum_nights = int(args[14]) if args[14] else None 
        self.number_of_reviews = int(args[15]) if args[15] else None
        self.review_scores_rating = float(args[16]) if args[16] else None
        self.instant_bookable = bool(args[17]) if args[17] else None
        self.cancellation_rate = int(args[18]) if args[18] else None
        self.reviews_per_month = float(args[19]) if args[19] else None
        self.fraud_count = int(args[20]) if args[20] else None
    
    def _STR(self, val):
        return str(val) if val is not None else 'ND'
    def _BOOL(self, val):
        return ('Yes' if val else 'No') if val is not None else 'ND'
    
    def __str__(self):
        return "Reviews\n\tScores Rating:"+self._STR(self.review_scores_rating)+"\n\tCount:"+self._STR(self.number_of_reviews)+ \
            "\n\tper Month:"+self._STR(self.reviews_per_month)+"\nPrice:"+self._STR(self.price)+"\nAmenities Price:"+ \
            self._STR(self.amenities_price)+ "\nMinimum Nights:"+self._STR(self.minimum_nights)+"\nMax Accomodation:"+ \
            self._STR(self.max_accomodation)+"\nCancellation Rate:"+ self._STR(self.cancellation_rate)+"\nCount\n\tBedroom:"+ \
            self._STR(self.bedroom_count)+"\n\tBed:"+self._STR(self.beds_count)+"\n\tBathroom:"+ self._STR(self.bathroom_count)+ \
            "\nType of\n\tProperty:"+self._STR(self.property_type)+"\n\tRoom:"+self._STR(self.room_type)+"\n\tBed:"+self._STR(self.bed_type)+ \
            "\nHost\n\tResponse Rate:"+self._STR(self.host_response_rate)+"\n\tTotal Listings:"+self._STR(self.host_total_listings_count)+ \
            "\nVerified\n\tHost Identity:"+ self._BOOL(self.host_identity_verified) + "\n\tLocation:"+ self._BOOL(self.location_verified) + \
            "\nCity UUID:"+ self.unique_city_id+ "\nFraud Count:"+ self.fraud_count+ "\nInstant Bookable:"+ self._BOOL(self.instant_bookable)+ '\n'

    def _print_attribute(self, val, width, is_last = False):
        print(val + ' ' * (width - len(val)), end='\n' if is_last else '|')

    def print_onTable(self, spaces):
        width = iter(spaces)
        self._print_attribute(self._STR(self.review_scores_rating), next(width))
        self._print_attribute(self._STR(self.number_of_reviews), next(width))
        self._print_attribute(self._STR(self.reviews_per_month), next(width))
        self._print_attribute(self._STR(self.price), next(width))
        self._print_attribute(self._STR(self.amenities_price), next(width))
        self._print_attribute(self._STR(self.max_accomodation), next(width))
        self._print_attribute(self._STR(self.minimum_nights), next(width))
        self._print_attribute(self._STR(self.cancellation_rate), next(width))
        self._print_attribute(self._STR(self.bedroom_count), next(width))
        self._print_attribute(self._STR(self.beds_count), next(width))
        self._print_attribute(self._STR(self.bathroom_count), next(width))
        self._print_attribute(self._STR(self.host_response_rate), next(width))
        self._print_attribute(self._STR(self.host_total_listings_count), next(width))
        self._print_attribute(self._STR(self.property_type), next(width))
        self._print_attribute(self._STR(self.room_type), next(width))
        self._print_attribute(self._STR(self.bed_type), next(width))
        self._print_attribute(self._BOOL(self.host_identity_verified), next(width))
        self._print_attribute(self._BOOL(self.location_verified), next(width))
        self._print_attribute(self._STR(self.unique_city_id), next(width))
        self._print_attribute(self._STR(self.fraud_count), next(width))
        self._print_attribute(self._BOOL(self.instant_bookable), next(width), True)
    
