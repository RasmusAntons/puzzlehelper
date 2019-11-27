from lib import urldefs
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession


async def test_urls(query):
    with FuturesSession() as session:
        futures = []
        for url_scheme in urldefs.get_matching(query):
            future = session.get(url_scheme.check_url())
            future.url_scheme = url_scheme
            futures.append(future)
        for future in as_completed(futures):
            print(future.result())
            yield future.url_scheme, future.result()
