import json
import decimal


class JSONEncoder(json.JSONEncoder):
     def default(self, obj):
          if isinstance(obj, decimal.Decimal):
               return str(obj)
          return json.JSONEncoder(JSONEncoder, self).default(obj)