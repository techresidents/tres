import json

from tres.encode import Encoder

class Query(object):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.data)

    def __str__(self):
        return json.dumps(self.to_json(), cls=Encoder)

    def to_json(self):
        return self.data

    def _to_list(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return [value]

class MatchAllQuery(Query):
    def __init__(self):
        data = { 'match_all': {} }
        super(MatchAllQuery, self).__init__(data)
    
    def __repr__(self):
        return '%s()' % self.__class__

class BoolQuery(Query):
    def __init__(self, must=None, must_not=None, should=None):
        super(BoolQuery, self).__init__(None)
        self.must_queries = []
        self.must_not_queries = []
        self.should_queries = []

        self.must(must)
        self.must_not(must_not)
        self.should(should)
    
    def __repr__(self):
        return '%s(must=%r, must_not=%r, should=%r)' % (
                self.__class__, self.must_queries,
                self.must_not_queries, self.should_queries)

    def must(self, query):
        if query is not None:
            self.must_queries.extend(self._to_list(query))
        return self

    def must_not(self, query):
        if query is not None:
            self.must_not_queries.extend(self._to_list(query))
        return self

    def should(self, query):
        if query is not None:
            self.should_queries.extend(self._to_list(query))
        return self

    def to_json(self):
        data = { 'bool': {} }
        if self.must_queries:
            queries = data['bool']['must'] = []
            for q in self.must_queries:
                queries.append(q)
        if self.must_not_queries:
            queries = data['bool']['must_not'] = []
            for q in self.must_not_queries:
                queries.append(q)
        if self.should_queries:
            queries = data['bool']['should'] = []
            for q in self.should_queries:
                queries.append(q)
        return data

class FilteredQuery(Query):
    def __init__(self, query, filter):
        super(FilteredQuery, self).__init__(None)
        self.query = query
        self.filter = filter

    def __repr__(self):
        return '%s(query=%r, filter=%r)' % (
                self.__class__, self.query, self.filter)
    
    def to_json(self):
        data = { 'filtered': {
            'query': self.query,
            'filter': self.filter
            }
        }
        return data

class MatchQuery(Query):
    def __init__(self, q, field):
        super(MatchQuery, self).__init__(None)
        self.q = q
        self.field = field

    def __repr__(self):
        return '%s(q=%r, field=%r)' % (
                self.__class__, self.q, self.field)
    
    def to_json(self):
        data = { 'match': {} }
        data['match'][self.field] = self.q
        return data

class MultiMatchQuery(Query):
    def __init__(self, q, fields):
        super(MultiMatchQuery, self).__init__(None)
        self.q = q
        self.fields = fields

    def __repr__(self):
        return '%s(q=%r, fields=%r)' % (
                self.__class__, self.q, self.fields)
    
    def to_json(self):
        data = { 'multi_match': {
            'query': self.q,
            'fields': self._parse_fields(self.fields)
            }
        }
        return data

    def _parse_fields(self, fields):
        result = []
        for field in self._to_list(fields):
            if isinstance(field, (list, tuple)):
                result.append('%s^%s' % (field[0], field[1]))
            else:
                result.append(field)
        return result

class RangeQuery(Query):
    def __init__(self, field, start=None, end=None,
            include_start=True, include_end=True):
        super(RangeQuery, self).__init__(None)
        self.field = field
        self.start = start
        self.end = end
        self.include_start = include_start
        self.include_end = include_end

    def __repr__(self):
        return '%s(field=%r, start=%r, end=%r)' % (
                self.__class__, self.field, self.start, self.end)

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

class TermQuery(Query):
    def __init__(self, field, value):
        super(TermQuery, self).__init__(None)
        self.field = field
        self.value = value

    def __repr__(self):
        return '%s(field=%r, value=%r)' % (
                self.__class__, self.field, self.value)
    
    def to_json(self):
        data = { 'term': {}}
        data['term'][self.field] = self.value
        return data

class TermsQuery(Query):
    def __init__(self, field, values):
        super(TermsQuery, self).__init__(None)
        self.field = field
        self.values = values

    def __repr__(self):
        return '%s(field=%r, values=%r)' % (
                self.__class__, self.field, self.values)

    def to_json(self):
        data = { 'terms': {}}
        data['terms'][self.field] = self._to_list(self.values)
        return data
