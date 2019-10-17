CODE_OK = 0
CODE_ACTION_NOT_FOUND = 1000
CODE_ARGUMENTS_ERROR = 1001


def make_result(code, msg):
    return dict(code=code, msg=msg)
