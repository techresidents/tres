import json

class Encoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(Encoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        to_json = getattr(obj, 'to_json', None)
        if to_json:
            return obj.to_json()
        else:
            return super(Encoder, self).default(obj)
