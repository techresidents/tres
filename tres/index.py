from contextlib import contextmanager
import json

from tres.encode import Encoder

class Index(object):
    def __init__(self, client, name, type=None):
        self.client = client
        self.name = name
        self.type = type

    def _to_list(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return [value]
    
    def get(self, key, type=None):
        type = type or self.type
        path = '%s/%s/%s' % (self.name, type, key)
        return self.client.send('GET', path)

    def mget(self, keys, type=None):
        type = type or self.type
        path = '%s/%s/_mget' % (self.name, type)
        data = json.dumps({'ids': keys})
        return self.client.send('GET', path, data)

    def put(self, key, doc, create=False, type=None):
        type = type or self.type
        path = '%s/%s/%s' % (self.name, type, key)
        if create:
            path += '/_create'
        data = json.dumps(doc)
        return self.client.send('PUT', path, data)

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

    def alias(self, add=None, remove=None):
        path = '_aliases'
        data = {'actions': [] }
        if add is not None:
            for new_alias in self._to_list(add):
                data['actions'].append({
                    'add': {'index': self.name, 'alias': new_alias }
                })
        if remove is not None:
            for old_alias in self._to_list(remove):
                data['actions'].append({
                    'remove': {'index': self.name, 'alias': old_alias }
                })
        data = json.dumps(data)
        print data
        return self.client.send('POST', path, data)

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

    def bulk(self, autoflush=20):
        bulk_index = BulkIndex(self.client, self.name, self.type, autoflush)
        return bulk_index


class BulkIndex(object):
    def __init__(self, client, name, type=None, autoflush=20):
        self.client = client
        self.name = name
        self.type = type
        self.autoflush = autoflush
        self.buffer = []
        self.errors = []

    def put(self, key, doc, create=False, type=None):
        op_type = 'create' if create else 'index'
        header = self._header(op_type, key, type)
        self.buffer.append((header, doc))
        self._autoflush()

    def delete(self, key, type=None):
        header = self._header('delete', key, type)
        self.buffer.append((header))
        self._autoflush()

    def flush(self):
        if not len(self.buffer):
            return None
        
        lines = []
        for item in self.buffer:
            if isinstance(item, tuple):
                lines.extend([json.dumps(i) for i in item])
            else:
                lines.append(json.dumps(item))

        path = '%s/_bulk' % self.name
        data = '\n'.join(lines) + '\n'
        result = self.client.send('POST', path, data)
        for item in result.get('items', []):
            for op in ['create', 'delete', 'index']:
                if op in item and 'error' in item[op]:
                    self.errors.append(item)
        self.buffer = []
        return result

    @contextmanager
    def flushing(self):
        try:
            yield self
        finally:
            self.flush()
    
    def clear_errors(self):
        self.errors = []

    def _header(self, op_type, key, type=None):
        type = type or self.type
        header = {}
        header[op_type] = {
            '_index': self.name,
            '_type': type,
            '_id': key
        }
        return header
    
    def _autoflush(self):
        if self.autoflush and len(self.buffer) >= self.autoflush:
            self.flush()
