from ..commons import cms4py_request_context
from . import result
from .ajax import register

actions = {
    "register.login_name_exists": register.login_name_exists,
    "register.user_exists": register.user_exists
}


async def do_action(action_name, context: cms4py_request_context.Cms4pyRequestContext):
    if action_name in actions:
        return await actions[action_name](context)
    else:
        return result.make_result(result.CODE_ACTION_NOT_FOUND, "Action not found.")
