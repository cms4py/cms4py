import inspect

import config
from cms4py import http
from cms4py.cache import ModulesCacheManager
from cms4py.actions import WsgiAction


async def handle_dynamic_request(scope, receive, send) -> bool:
    data_sent = False
    request_path: str = scope['path']

    # 将请求路径分拆为 controller 和 action，例如：/user/list_all 请求
    # 对应的 controller 是 user， action 是 list_all
    tokens = request_path.split("/")
    tokens_len = len(tokens)
    # 指定默认的控制器名
    controller_name = config.DEFAULT_CONTROLLER
    if tokens_len >= 2:
        controller_name = tokens[1] or config.DEFAULT_CONTROLLER
    # 指定默认的函数名
    action_name = config.DEFAULT_ACTION
    if tokens_len >= 3:
        action_name = tokens[2] or config.DEFAULT_ACTION

    controller_object = await ModulesCacheManager.get_instance().get_data(
        f"{config.APP_DIR_NAME}.{config.CONTROLLERS_DIR_NAME}.{controller_name}"
    )

    if controller_object:
        # 根据 action_name 获取指定的成员
        action = getattr(controller_object, action_name, None)
        if action:
            # 构造 HTTP 请求对象，便于后续操作
            req = http.Request(scope, receive)
            # 构造 HTTP 响应对象，便于后续操作
            res = http.Response(req, send)
            req._controller = controller_name
            req._action = action_name

            # 将 action 后的路径参数记录在 req.args 中
            req._args = tokens[3:] if len(tokens) > 3 else []
            # 如果 action 是类定义，则先将类实例化再执行
            if inspect.isclass(action):
                the_action_instance = action()
                if not isinstance(the_action_instance, WsgiAction):
                    # If the action is a WsgiAction, there is no need to parse form or load language dict
                    await req._parse_form()
                    # 预加载语言表
                    await res._load_language_dict()
                await the_action_instance(req, res)
            # 否则把 action 当作函数对待直接执行
            else:
                await req._parse_form()
                # 预加载语言表
                await res._load_language_dict()
                await action(req, res)
            data_sent = res.body_sent
    return data_sent
