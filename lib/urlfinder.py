import re
import urllib.request

url_schemes = [
    ('pastebin.com', 'https://pastebin.com/{}', r'^[a-zA-Z]{8}$', None),
    ('youtube.com', 'https://www.youtube.com/watch?v={}', r'^[a-zA-Z0-9]{11}$', None),
    ('bit.ly', 'https://bit.ly/{}', r'^[a-zA-Z0-9]{7}$', None),
    ('imgur.com', 'https://imgur.com/a/{}', r'^[a-zA-Z0-9]{5,7}$', None),
    ('imgur.com', 'https://imgur.com/{}', r'^[a-zA-Z0-9]{5,7}$', None),
    ('bit.do', 'http://bit.do/{}', r'^[a-zA-Z0-9]+$', lambda u, r: u != r.geturl()),
    ('mega.nz', 'https://mega.nz/{}', r'^#![a-zA-Z0-9]{8}![a-zA-Z0-9]{43}$', None)
]


def test_urls(s):
    for label, frmt, pattern, validator in url_schemes:
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
