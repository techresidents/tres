from tres.filter import RangeFilter, TermFilter

class Facets(object):
    def __init__(self, facets=None):
        self.data = {}
        if facets:
            for key, facet in facets.items():
                self.data[key] = facet
    
    def to_json(self):
        return self.data

    def add(self, key, facet):
        self.data[key] = facet
        return self

class Facet(object):
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return self.data

    def _to_list(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return [value]

class RangeFacet(Facet):
    class Range(object):
        def __init__(self, start=None, end=None,
                include_start=True, include_end=True, name=None):
            self.start = start
            self.end = end
            self.include_start = include_start
            self.include_end = include_end
            self.name = name
        
        def to_json(self):
            result = {
                'include_lower': self.include_start,
                'include_upper': self.include_end
            }
            if self.start is not None:
                result['from'] = self.start
            if self.end is not None:
                result['to'] = self.end
            return result

    def __init__(self, field, ranges=None):
        super(RangeFacet, self).__init__(None)
        self.field = field
        self.ranges = ranges or []
    
    def add_range(self, start=None, end=None,
            include_start=True, include_end=True, name=None):
        r = self.Range(start, end, include_start, include_end, name)
        self.ranges.append(r)
        return self

    def to_json(self):
        data = { 'range': {} }
        data['range'][self.field] = self._to_list(self.ranges)
        return data

class TermsFacet(Facet):
    def __init__(self, field, size=10):
        super(TermsFacet, self).__init__(None)
        self.field = field
        self.size = size

    def to_json(self):
        data = {'terms': {} }
        data['terms'][self.field] = {
            'field': self.field,
            'size': self.size
        }
        return data

class FacetResultFactory(object):
    def create(self, search, name, data):
        type = data.get('_type')
        search_facet = search.facets.data.get(name)

        if type == 'terms':
            result = TermsFacetResult(name, search_facet, data)
        elif type == 'range':
            result = RangeFacetResult(name, search_facet, data)
        else:
            result = FacetResult(name, search_facet, data)
        return result

class FacetResult(object):
    def __init__(self, name, search_facet, data):
        self.name = name
        self.search_facet = search_facet
        self.field = search_facet.field
        self.data = data or {}
        self.items = []
    
    @property
    def type(self):
        return self.data.get('_type')

class RangeFacetResult(FacetResult):
    def __init__(self, name, search_facet, data):
        super(RangeFacetResult, self).__init__(name, search_facet, data)
        search_ranges = search_facet.ranges
        result_ranges = data.get('ranges')
        for search_range, result_range in zip(search_ranges, result_ranges):
            self.items.append(self._create_item(search_range, result_range))
    
    @property
    def ranges(self):
        return self.data.get('ranges')

    def _create_item(self, search_range, result_range):
        start = search_range.start
        end = search_range.end
        include_start = search_range.include_start
        include_end = search_range.include_end
        name = search_range.name
        if name is None:
            if start is not None and end is not None:
                name = '%s to %s' % (start, end)
            elif start is not None:
                name = '%s+' % start
            else:
                name = '<= %s' % end 
        
        filter = RangeFilter(self.field, start, end, include_start, include_end)
        
        return FacetResultItem(name, result_range.get('count'), filter)

class TermsFacetResult(FacetResult):
    def __init__(self, name, search_facet, data):
        super(TermsFacetResult, self).__init__(name, search_facet, data)
        for term in data.get('terms'):
            self.items.append(self._create_item(term))
    
    @property
    def terms(self):
        return self.data.get('terms')

    def _create_item(self, term):
        filter = TermFilter(self.field, term.get('term'))
        return FacetResultItem(term.get('term'), term.get('count'), filter)

class FacetResultItem(object):
    def __init__(self, name, count, filter):
        self.name = name
        self.count = count
        self.filter = filter
