#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   query.py -
#
#   00/00/00: -created
#

import etl as ETL
import numpy

class QueryElement:
    def __init__(self, index, value):
        self.index = index
        self.value = value

    def __lt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.value < other
        return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.value > other
        return self.value > other.value

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.value == other
        return self.value == other.value
    
    def __int__(self):
        return self.index


class Query:
    def __init__(self, label = None, graph_callback = None):
        self._query_buffer = []
        self._query = None
        self._scope = None
        self._cache_bitset = None
        self.label = label
        self.graph_callback = graph_callback

    def push_to_buffer(self, index, value):
        if value is None:
            return
        self._query_buffer.append(QueryElement(index, value))

    def init(self):
        if self._query is not None:
            return
        self._query = numpy.sort(numpy.array(self._query_buffer, dtype=QueryElement), kind="mergesort")
        self._query_buffer = None

    def __iter__(self):
        if self._scope is None:
            return iter(self._query)
        return iter(self._query[self._scope])

    def __getitem__(self, p_slice):
        return self._query[p_slice]

    def get_size(self):
        if self._scope is None:
            return len(self._query)
        if self._scope.start is None:
            return self._scope.stop
        if self._scope.stop is None:
            return len(self._query) - self._scope.start
        return self._scope.stop - self._scope.start

    def get_max(self):
        return self._query[-1].value
    
    def get_min(self):
        return self._query[0].value
    
    def clear(self):
        self._scope = None
        self._cache_bitset = None

    def _get_bitset_dirty(self) -> numpy.ndarray:
        res = numpy.full(ETL.AirbnbETL.get_data_size(), False)
        if self._cache_bitset is not None:
            return self._cache_bitset
        for el in self:
            res[int(el)] = True
        self._cache_bitset = numpy.array(res)
        return self._cache_bitset

    def combine_filter(self, filter) -> numpy.ndarray:
        bitset = self._get_bitset_dirty()
        res = []
        for i in filter:
            if bitset[int(i)]:
                res.append(int(i))
        return numpy.array(res)
    
    def order_data(self, filter): # -> [QueryElement]
        bitset = numpy.full(ETL.AirbnbETL.get_data_size(), False)
        for i in filter:
            bitset[int(i)] = True
        res = []
        for el in self:
            if bitset[int(el)]:
                res.append(el)
        return res
        

class RangeQuery(Query):
    def find_range(self, min, max):
        self._scope = slice(numpy.searchsorted(self._query, min), numpy.searchsorted(self._query, max, side="right"), None)
        self._cache_bitset = None
        return self
    def filter(self, *args):
        return self.find_range(*args)

class GreaterThanQuery(Query):
    def find_greater_than(self, number):
        self._scope = slice(numpy.searchsorted(self._query, number), len(self._query), None)
        self._cache_bitset = None
        return self
    def filter(self, *args):
        return self.find_greater_than(*args)

class LessThanQuery(Query):
    def find_less_than(self, number):
        self._scope = slice(0, numpy.searchsorted(self._query, number, side="right"), None)
        self._cache_bitset = None
        return self
    def filter(self, *args):
        return self.find_less_than(*args)

class FindQuery(Query):
    def find_equal_to(self, number):
        self._scope = slice(numpy.searchsorted(self._query, number), numpy.searchsorted(self._query, number, side="right"), None)
        self._cache_bitset = None
        return self
    def filter(self, *args):
        return self.find_equal_to(*args)
