from .url import URL
import inspect


async def has_membership(context, role):
    if not context.current_user:
        return False
    db = context.db
    return not (await db(
        (db.member_group.role == role) &
        (db.membership.user_id == context.current_user["id"]) &
        (db.member_group.id == db.membership.group_id)
    ).isempty())


def require_login(func):
    async def wrapper(context, *args, **kwargs):
        if context.current_user:
            return await func(context, *args, **kwargs)
        else:
            context.redirect(URL("user", "login", vars=dict(_next=context.get_request_uri())))

    return wrapper


def require_membership(role):
    def outer(func):
        async def inner(context, *args, **kwargs):
            if context.current_user:
                if await has_membership(context, role):
                    await func(context, *args, **kwargs)
                else:
                    context.write("Access Denied")
            else:
                context.redirect(URL("user", "login", vars=dict(_next=context.get_request_uri())))

        return inner

    return outer


def requires(condition):
    def outer(func):
        async def inner(context, *args, **kwargs):
            if (inspect.isawaitable(condition) and await condition) or condition:
                return await func(context, *args, **kwargs)
            else:
                context.write("Access Denied")

        return inner

    return outer
