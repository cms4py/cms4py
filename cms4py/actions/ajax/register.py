from ...commons.request_context import RequestContext
from .. import result


async def user_exists_by_field(context: RequestContext, field_name):
    field_value = context.get_argument(field_name, None)
    if field_value:
        db = context.db
        exists = not await db(db.user[field_name] == field_value).isempty()
        result_data = result.make_result(result.CODE_OK, "OK")
        result_data["exists"] = exists
        return result_data
    else:
        return result.make_result(result.CODE_ARGUMENTS_ERROR, "Arguments error")


async def login_name_exists(context: RequestContext):
    return await user_exists_by_field(context, "login_name")


async def user_exists(context: RequestContext):
    field_name = context.get_argument("field_name", None)
    if field_name:
        return await user_exists_by_field(context, field_name)
    else:
        return result.make_result(result.CODE_ARGUMENTS_ERROR, "Arguments error")
