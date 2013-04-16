
class Filter(object):
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return self.data

    def _to_list(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return [value]

class BoolFilter(Filter):
    def __init__(self, must=None, must_not=None, should=None):
        data = { 'bool': {} }
        super(BoolFilter, self).__init__(data)

        self.must(must)
        self.must_not(must_not)
        self.should(should)

    def must(self, filter):
        self._add_filter(filter, 'must')
        return self

    def must_not(self, filter):
        self._add_filter(filter, 'must_not')
        return self

    def should(self, filter):
        self._add_filter(filter, 'should')
        return self

    def _add_filter(self, filter, key):
        if filter:
            filters = self.data['bool'].get(key, None)
            if filters is None:
                filters = []
                self.data['bool'][key] = filters
            filters.extend(self._to_list(filters))

class RangeFilter(Filter):
    def __init__(self, field, start=None, end=None,
            include_start=True, include_end=True):
        data = { 'range': {} }
        data['range'][field] = {
            'include_lower': include_start,
            'include_upper': include_end
        }
        if start:
            data['range'][field]['from'] = start
        if end:
            data['range'][field]['to'] = end

        super(RangeFilter, self).__init__(data)

class TermFilter(Filter):
    def __init__(self, field, value):
        data = { 'term': {}}
        data['term'][field] = value
        super(TermFilter, self).__init__(data)

class TermsFilter(Filter):
    def __init__(self, field, values):
        data = { 'terms': {}}
        data['terms'][field] = self._to_list(values)
        super(TermsFilter, self).__init__(data)
