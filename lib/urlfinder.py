import re
import urllib.request
import hashlib


def check_itstoohard(u, r):
    return hashlib.md5(r.read().split(b'</script>')[-1]).digest() != b'P\x9b\xaa2\x070n:\x89\x16\xfbB\xcd\x8dV\x1c'


url_schemes = [
    ('pastebin.com', 'https://pastebin.com/{}', None, r'^[a-zA-Z]{8}$', None),
    ('youtube.com', 'https://www.youtube.com/watch?v={}', None, r'^[a-zA-Z0-9]{11}$', None),
    ('bit.ly', 'https://bit.ly/{}', None, r'^[a-zA-Z0-9]{7}$', None),
    ('imgur.com', 'https://imgur.com/a/{}', None, r'^[a-zA-Z0-9]{5,7}$', None),
    ('imgur.com', 'https://imgur.com/{}', None, r'^[a-zA-Z0-9]{5,7}$', None),
    ('bit.do', 'http://bit.do/{}', None, r'^[a-zA-Z0-9]+$', lambda u, r: u != r.geturl()),
    ('mega.nz', 'https://mega.nz/{}', None, r'^#![a-zA-Z0-9]{8}![a-zA-Z0-9]{43}$', None),
    ('discord.gg', 'https://discordapp.com/api/v6/invites/{}', None, r'^[a-zA-Z0-9]+$', None),
    ('itstoohard.com', 'http://www.itstoohard.com/puzzle/{}', None, r'^[a-zA-Z0-9]{8}$', check_itstoohard)
]


def test_urls(s):
    for label, frmt, disp_frmt, pattern, validator in url_schemes:
        if re.match(pattern, s):
            url = frmt.format(s)
            try:
                r = urllib.request.urlopen(url)
                if validator is None or validator(url, r):
                    yield (label, url, f'success: {r.code}')
                else:
                    yield (label, url, f'failed: {r.code}')
            except urllib.error.HTTPError as e:
                yield (label, url, f'error: {e.code}')
