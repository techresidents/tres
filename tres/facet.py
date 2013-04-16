
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
    def __init__(self, field, ranges):
        data = { 'range': {} }
        data['range'][field] = {
            'ranges': self._to_list(ranges)
        }
        super(RangeFacet, self).__init__(data)

class TermsFacet(Facet):
    def __init__(self, field, size=10):
        data = {'terms': {} }
        data['terms'][field] = {
            'field': field,
            'size': size
        }
        super(TermsFacet, self).__init__(data)
