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

    def __len__(self):
        return len(self.data)

    def to_json(self):
        """ Convert object to json format """
        json = []
        for field, direction in self.data:
            json.append({field: direction})
        return json

    def add(self, es_field, direction='asc'):
        """ Add a field to sort by.

         Args:
            es_field: field name string
            direction: direction string (expects 'asc' or 'desc')

        """
        self.data.append( (es_field, direction.lower()) )
        return self