import json

from tres.encode import Encoder

class Sort(object):

    def __init__(self, data=None):
        """ Sort constructor.

        Args:
            data: A list of tuples to sort by. The tuple should be a
            (field_name, sort_direction) pair. You can optionally pass
            just a list of field names, which will then sort each field
            in ascending order.

        This object maintains a list of tuples to sort by.
        For example: [('title', 'ASC')]

        """
        self.data = []
        if data:
            for field in data:
                if isinstance(field, (list, tuple)):
                    if len(field) > 1:
                        self.add(field[0], field[1])
                    else:
                        self.add(field[0])
                else:
                    self.add(field)

    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.data)

    def __str__(self):
        return json.dumps(self.to_json(), cls=Encoder)

    def to_json(self):
        """ Convert object to json format """
        json = []
        for tup in self.data:
            json.append({tup[0]: tup[1]})
        return json

    def add(self, es_field, direction='asc'):
        """ Add a field to sort by.

         Args:
            es_field: field name string
            direction: direction string (expects 'asc' or 'desc')

        """
        self.data.append( (es_field, self._to_es_direction(direction)) )
        return self

    def length(self):
        """ Returns the number of fields to sort by."""
        return len(self.data)

    def _to_es_direction(self, direction):
        """ Convert sorting direction string into a string ES can understand.

        Args:
            direction: direction string
        Returns:
            Returns 'asc' by default.
            Returns 'desc' for descending sorts.

        ES supports the following sort direction strings:
            'asc' for ascending
            'desc' for descending

        """
        es_direction = 'asc'
        if direction.lower() == 'desc':
            es_direction = 'desc'
        return es_direction