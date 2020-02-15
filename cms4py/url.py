import urllib.parse


def URL(*parts, vars=None, host=None, host_name=None, port=80, scheme="https://"):
    """
     host中应包含端口号，传入host则不需要传入port，
     host_name中应不包括端口号，在传入host_name同时需要传入port（默认值为80）
    """
    str_arr = []
    for v in parts:
        if isinstance(v, str):
            str_arr.append(v)
        else:
            str_arr.append(str(v))
    url = ('/' if str_arr[0][0] != '/' else "") + "/".join(str_arr)
    if vars:
        filtered_vars = dict()
        for k, v in vars.items():
            if v:
                filtered_vars[k] = v
        vars = filtered_vars
    if vars:
        url += '?' + '&'.join('%s=%s' % (k, urllib.parse.quote(str(v))) for k, v in vars.items())

    if host:
        url = f"{scheme}{host}{url}"
        return url
    if host_name:
        url = f"{scheme}{host_name}:{port}{url}"
    return url
