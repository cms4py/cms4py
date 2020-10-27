

def parse_url_pairs(query_string: bytes):
    """
    将 url 字符串解码为字典，因为可能存在多条同键名的数据，
    所以每一个字段所对应的是一个列表
    :param query_string:
    :return:
    """

    params = {}

    # url 字符串是以 & 符号连接的，如：name=yunp&age=20
    # 以 & 符号分割出的字符串数组如：[name=yunp,age=20]
    # 之后再用等号分别分割每一个字符串，即可得到键值对
    tokens = query_string.split(b"&")
    for t in tokens:
        kv = t.split(b"=")
        if len(kv) == 2:
            k = kv[0]
            v = kv[1]
            if k not in params:
                params[k] = []
            params[k].append(v)
    return params
