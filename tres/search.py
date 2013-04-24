from trpycore.util.attribute import xgetattr

from tres.facet import FacetResultFactory

class Search(object):
    def __init__(self, query=None, filter=None, facets=None, start=None, size=None):
        self.query = query
        self.filter = filter
        self.facets = facets
        self.start = start
        self.size = size

    def to_json(self):
        result = {}
        if self.query is not None:
            result['query'] = self.query
        if self.filter is not None:
            result['filter'] = self.filter
        if self.facets is not None:
            result['facets'] = self.facets
        if self.start is not None:
            result['from'] = self.start
        if self.size is not None:
            result['size'] = self.size
        
        return result


class SearchResult(object):
    def __init__(self, search, data):
        self.search = search
        self.data = data or {}
        self.hits = []
        self.facets = {}

        for hit in xgetattr(data, 'hits.hits'):
            self.hits.append(SearchHit(hit))
        
        factory = FacetResultFactory()
        result_facets = data.get('facets') or {}
        for name, facet in result_facets.items():
            self.facets[name] = factory.create(search, name, facet)

    @property
    def hits_total(self):
        return xgetattr(self.data, 'hits.total')


class SearchHit(object):
    def __init__(self, data):
        self.data = data or {}

    @property
    def index(self):
        return self.data.get('_index')

    @property
    def type(self):
        return self.data.get('_type')

    @property
    def id(self):
        return self.data.get('_id')

    @property
    def score(self):
        return self.data.get('_score')
    
    @property
    def source(self):
        return self.data.get('_source')
