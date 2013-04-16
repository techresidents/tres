class Query(object):
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return self.data

    def _to_list(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return [value]

class BoolQuery(Query):
    def __init__(self, must=None, must_not=None, should=None):
        data = { 'bool': {} }
        super(BoolQuery, self).__init__(data)

        self.must(must)
        self.must_not(must_not)
        self.should(should)

    def must(self, query):
        self._add_query(query, 'must')
        return self

    def must_not(self, query):
        self._add_query(query, 'must_not')
        return self

    def should(self, query):
        self._add_query(query, 'should')
        return self

    def _add_query(self, query, key):
        if query:
            queries = self.data['bool'].get(key, None)
            if queries is None:
                queries = []
                self.data['bool'][key] = queries
            queries.extend(self._to_list(query))

class FilteredQuery(Query):
    def __init__(self, query, filter):
        data = { 'filtered': {
            'query': query,
            'filter': filter
            }
        }
        super(FilteredQuery, self).__init__(data)

class MatchQuery(Query):
    def __init__(self, q, field):
        data = { 'match': {} }
        data['match'][field] = q
        super(MatchQuery, self).__init__(data)

class MultiMatchQuery(Query):
    def __init__(self, q, fields):
        data = { 'multi_match': {
            'query': q,
            'fields': self._parse_fields(fields)
            }
        }
        super(MultiMatchQuery, self).__init__(data)
    
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
        data = { 'range': {} }
        data['range'][field] = {
            'include_lower': include_start,
            'include_upper': include_end
        }
        if start:
            data['range'][field]['from'] = start
        if end:
            data['range'][field]['to'] = end

        super(RangeQuery, self).__init__(data)

class TermQuery(Query):
    def __init__(self, field, value):
        data = { 'term': {}}
        data['term'][field] = value
        super(TermQuery, self).__init__(data)

class TermsQuery(Query):
    def __init__(self, field, values):
        data = { 'terms': {}}
        data['terms'][field] = self._to_list(values)
        super(TermsQuery, self).__init__(data)


