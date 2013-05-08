import Queue

from trpycore.pool.queue import QueuePool

class ESClientPool(QueuePool):
    """ESClient pool.

    Example usage:
        with pool.get() as es_client:
            users = es_client.index('users', 'user')
            users.status()
    """
    
    def __init__(self, es_client_factory, size, queue_class=Queue.Queue):
        """ESClientPool constructor.

        Args:
            es_client_factory: Factory object to create ESClient objects.
            size: Number of objects to include in pool.
            queue_class: Optional Queue class. If not provided, will
                default to Queue.Queue. The specified class must
                have a no-arg constructor and provide a get(block, timeout)
                method.
        """
        self.es_client_factory = es_client_factory
        self.size = size
        self.queue_class = queue_class
        super(ESClientPool, self).__init__(
                self.size,
                factory=self.es_client_factory,
                queue_class=self.queue_class)
