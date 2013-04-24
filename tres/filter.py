
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
        super(BoolFilter, self).__init__(None)
        self.must_filters = []
        self.must_not_filters = []
        self.should_filters = []

        self.must(must)
        self.must_not(must_not)
        self.should(should)

    def must(self, filter):
        if filter is not None:
            self.must_filters.extend(self._to_list(filter))
        return self

    def must_not(self, filter):
        if filter is not None:
            self.must_not_filters.extend(self._to_list(filter))
        return self

    def should(self, filter):
        if filter is not None:
            self.should_filters.extend(self._to_list(filter))
        return self

    def to_json(self):
        data = { 'bool': {} }
        if self.must_filters:
            filters = data['bool']['must'] = []
            for f in self.must_filters:
                filters.append(f)
        if self.must_not_filters:
            filters = data['bool']['must_not'] = []
            for f in self.must_not_filters:
                filters.append(f)
        if self.should_filters:
            filters = data['bool']['should'] = []
            for f in self.should_filters:
                filters.append(f)
        return data

class RangeFilter(Filter):
    def __init__(self, field, start=None, end=None,
            include_start=True, include_end=True):
        super(RangeFilter, self).__init__(None)
        self.field = field
        self.start = start
        self.end = end
        self.include_start = include_start
        self.include_end = include_end

    def to_json(self):
        data = { 'range': {} }
        data['range'][self.field] = {
            'include_lower': self.include_start,
            'include_upper': self.include_end
        }
        if self.start is not None:
            data['range'][self.field]['from'] = self.start
        if self.end is not None:
            data['range'][self.field]['to'] = self.end
        return data

class TermFilter(Filter):
    def __init__(self, field, value):
        super(TermFilter, self).__init__(None)
        self.field = field
        self.value = value

    def to_json(self):
        data = { 'term': {}}
        data['term'][self.field] = self.value
        return data

class TermsFilter(Filter):
    def __init__(self, field, values):
        super(TermsFilter, self).__init__(None)
        self.field = field
        self.values = values

    def to_json(self):
        data = { 'terms': {}}
        data['terms'][self.field] = self._to_list(self.values)
        return data
