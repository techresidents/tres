import json

from tres.index import Index, BulkIndex
from trhttp.rest.client import RestClient

class ESClient(object):
    def __init__(
            self,
            endpoint,
            timeout=10,
            keepalive=True,
            rest_client_class=None):
        
        rest_client_class = rest_client_class or RestClient

        self.rest_client = rest_client_class(
                endpoint=endpoint,
                authenticator=None,
                timeout=timeout,
                keepalive=keepalive)
 
    def create_index(self, name, settings=None, mappings=None):
        data = {}
        if settings is not None:
            data['settings'] = settings

        if mappings is not None:
            data['mappings'] = mappings
        
        data = json.dumps(data)
        return self.send('POST', name, data)


    def get_index(self, name, type=None):
        return Index(self, name, type)

    def get_bulk_index(self, name, type=None, autoflush=20):
        return BulkIndex(self, name, type, autoflush)

    def delete_index(self, name):
        return self.send('DELETE', name)

    def send(self, method, path, data=None, headers=None):
        response_context = self.rest_client.send_request(method, path, data, headers)
        with response_context as response:
            data = response.read()
            result = json.loads(data)
        return result

