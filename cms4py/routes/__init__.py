from . import index, user, rest, session_counter

routes = [
    (r"/", index.Index),
    (r"/user/register", user.Register),
    (r"/user/login", user.Login),
    (r"/user/profile", user.Profile),
    (r"/user/logout", user.Logout),
    (r"/user/ajax_info", user.AjaxInfo),
    (r"/rest/db_api/([^/]+)/?([^/]*)", rest.DbAPI),
    (r"/rest/action/([^/]+)", rest.Action),
    (r"/session_counter", session_counter.SessionCounter),
]
