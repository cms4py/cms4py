import urllib.parse


def URL(*parts, vars=None, host=None, scheme="https://"):
    url = ('/' if parts[0][0] != '/' else "") + "/".join(parts)
    if vars:
        url += '?' + '&'.join('%s=%s' % (k, urllib.parse.quote(str(v))) for k, v in vars.items())

    if host:
        url = scheme + host + url
    return url
