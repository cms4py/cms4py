from . import index, user, rest, session_counter
from .dashboard import index as dashboard_index
from .dashboard import site
from .dashboard import user as dashboard_user

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
    (r"/dashboard", dashboard_index.Index),
    (r"/dashboard/index", dashboard_index.Index),
    (r"/dashboard/site/versions", site.Versions),
    (r"/dashboard/user/all_users", dashboard_user.AllUsers),
    (r"/dashboard/user/all_groups", dashboard_user.AllGroups),
    (r"/dashboard/user/memberships", dashboard_user.Memberships),
]
