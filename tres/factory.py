from trpycore.factory.base import Factory

from tres.client import ESClient

class ESClientFactory(Factory):
    """Factory for creating ESClient objects."""

    def __init__(self,
            endpoint,
            timeout=10,
            keepalive=True,
            rest_client_class=None):
        """ESClientFactory constructor.

        Args:
            endpoint: ES endpoint - 'http://localhost:9200'
            timeout: Socket timeout in seconds
            keepalive: Boolean indicating if connection should be kept
                open between requests
            rest_client_class: optional rest client class
        """
        self.endpoint = endpoint
        self.timeout = timeout
        self.keepalive = keepalive
        self.rest_client_class = rest_client_class

    def create(self):
        """Return instance of ESClient object."""
        return ESClient(endpoint=self.endpoint,
                timeout=self.timeout,
                keepalive=self.keepalive,
                rest_client_class=self.rest_client_class)
