from . import index, user, rest

routes = [
    (r"/", index.Index),
    (r"/user/register", user.Register),
    (r"/rest/db_api/([^/]+)/?([^/]*)", rest.DbAPI),
    (r"/rest/action/([^/]+)", rest.Action),
]
