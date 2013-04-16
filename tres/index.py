import json

from tres.encode import Encoder

class Index(object):
    def __init__(self, client, name, type=None):
        self.client = client
        self.name = name
        self.type = type
    
    def get(self, key, type=None):
        type = type or self.type
        path = '%s/%s/%s' % (self.name, type, key)
        return self.client.send('GET', path)

    def mget(self, keys, type=None):
        type = type or self.type
        path = '%s/%s/_mget' % (self.name, type)
        data = json.dumps({'ids': keys})
        return self.client.send('GET', path, data)

    def put(self, key, doc, type=None):
        type = type or self.type
        path = '%s/%s/%s' % (self.name, type, key)
        data = json.dumps(doc)
        return self.client.send('GET', path, data)

    def update(self, key, params, type=None):
        type = type or self.type
        path = '%s/%s/%s' % (self.name, type, key)
        data = json.dumps({'params': params})
        return self.client.send('POST', path, data)

    def delete(self, key, type=None):
        type = type or self.type
        path = '%s/%s/%s' % (self.name, type, key)
        return self.client.send('DELETE', path)

    def search(self, query, filter=None, facets=None,
            start=None, size=None, type=None):
        type = type or self.type
        path = '%s/%s/_search' % (self.name, type)

        #construct search
        search = {}
        if query:
            search['query'] = query
        if filter:
            search['filter'] = filter
        if facets:
            search['facets'] = facets
        if start:
            search['from'] = start
        if size:
            search['size'] = size
    
        data = json.dumps(search, cls=Encoder)
        return self.client.send('GET', path, data)

    def flush(self):
        path = '%s/_flush' % self.name
        return self.client.send('POST', path)

    def refresh(self):
        path = '%s/_refresh' % self.name
        return self.client.send('POST', path)

    def status(self):
        path = '%s/_status' % self.name
        return self.client.send('GET', path)

    def stats(self):
        path = '%s/_stats' % self.name
        return self.client.send('GET', path)
