import re
import hashlib


class UrlScheme:
    label = None
    pattern = None
    check_format = None
    display_format = None

    def __init__(self, query):
        self.query = query

    def check_url(self):
        return self.check_format.format(self.query)

    def display_url(self):
        if self.display_format:
            return self.display_format.format(self.query)
        else:
            return self.check_format.format(self.query)

    def is_valid_response(self, response):
        return response.ok

    @classmethod
    def is_candidate(cls, query):
        return re.match(cls.pattern, query)


class UrlPastebin(UrlScheme):
    label = 'pastebin.com'
    pattern = r'^[a-zA-Z]{8}$'
    check_format = 'https://pastebin.com/{}'


class UrlYoutube(UrlScheme):
    label = 'youtube.com'
    pattern = r'^[a-zA-Z0-9]{11}$'
    check_format = 'https://www.youtube.com/watch?v={}'


class UrlBitly(UrlScheme):
    label = 'bit.ly'
    pattern = r'^[a-zA-Z0-9]{7}$'
    check_format = 'https://bit.ly/{}'


class UrlImgur(UrlScheme):
    label = 'imgur.com'
    pattern = r'^[a-zA-Z0-9]{5,7}$'
    check_format = 'https://imgur.com/a/{}'


class UrlImgurAlbum(UrlScheme):
    label = 'imgur.com/a'
    pattern = r'^[a-zA-Z0-9]{5,7}$'
    check_format = 'https://imgur.com/{}'


class UrlBitdo(UrlScheme):
    label = 'bit.do'
    pattern = r'^[a-zA-Z0-9]+$'
    check_format = 'http://bit.do/{}'

    def is_valid_response(self, response):
        return self.check_url() != response.url


class UrlMega(UrlScheme):
    label = 'mega.nz'
    pattern = r'^#![a-zA-Z0-9]{8}!([a-zA-Z0-9]{43})?$'
    check_format = 'https://mega.nz/{}'


class UrlDiscord(UrlScheme):
    label = 'discord.gg'
    pattern = r'^[a-zA-Z0-9]+$'
    check_format = 'https://discordapp.com/api/v6/invites/{}'
    display_format = 'https://discord.gg/{}'


class UrlItstoohard(UrlScheme):
    label = 'itstoohard.com'
    pattern = r'^[a-zA-Z0-9]{8}$'
    check_format = 'http://www.itstoohard.com/puzzle/{}'

    def is_valid_response(self, response):
        return hashlib.md5(response.content.split(b'</script>')[-1]).digest() != b'P\x9b\xaa2\x070n:\x89\x16\xfbB\xcd\x8dV\x1c'


url_schemes = [UrlPastebin, UrlYoutube, UrlBitly, UrlImgur, UrlImgurAlbum, UrlBitdo, UrlMega, UrlDiscord, UrlItstoohard]


def get_matching(query):
    return (url_scheme(query) for url_scheme in url_schemes if url_scheme.is_candidate(query))
