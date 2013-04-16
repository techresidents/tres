import json

from tres.index import Index
from trhttp.rest.client import RestClient

class ESClient(object):
    def __init__(
            self,
            endpoint,
            timeout=10,
            keepalive=True,
            rest_client_class=RestClient):
        
        self.rest_client = rest_client_class(
                endpoint=endpoint,
                authenticator=None,
                timeout=timeout,
                keepalive=keepalive)
                
    def index(self, name, type=None):
        return Index(self, name, type)

    def send(self, method, path, data=None, headers=None):
        response = self.rest_client.send_request(method, path, data, headers)
        result = json.loads(response.read())
        return result
