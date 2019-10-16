from . import index
from . import user

routes = [
    (r"/", index.Index),
    (r"/user/register", user.Register),
]
