import tornado.escape
import json.decoder

try:
    print(tornado.escape.json_decode("a"))
except json.decoder.JSONDecodeError:
    pass
