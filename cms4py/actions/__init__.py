from ..commons import Cms4pyRequestContext
from . import result
from .ajax import register

actions = {
    "register.login_name_exists": register.login_name_exists,
    "register.user_exists": register.user_exists
}


def do_action(action_name, context: Cms4pyRequestContext.Cms4pyRequestContext):
    if action_name in actions:
        return actions[action_name](context)
    else:
        return result.make_result(result.CODE_ACTION_NOT_FOUND, "Action not found.")
