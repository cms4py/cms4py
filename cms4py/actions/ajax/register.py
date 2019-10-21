from ...commons.Cms4pyRequestContext import Cms4pyRequestContext
from .. import result


def user_exists_by_field(context: Cms4pyRequestContext, field_name):
    field_value = context.get_argument(field_name, None)
    if field_value:
        db = context.db
        exists = not db(db.user[field_name] == field_value).isempty()
        result_data = result.make_result(result.CODE_OK, "OK")
        result_data["exists"] = exists
        return result_data
    else:
        return result.make_result(result.CODE_ARGUMENTS_ERROR, "Arguments error")


def login_name_exists(context: Cms4pyRequestContext):
    return user_exists_by_field(context, "login_name")


def user_exists(context: Cms4pyRequestContext):
    field_name = context.get_argument("field_name", None)
    if field_name:
        return user_exists_by_field(context, field_name)
    else:
        return result.make_result(result.CODE_ARGUMENTS_ERROR, "Arguments error")
