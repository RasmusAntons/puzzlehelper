from channels.generic.websocket import AsyncWebsocketConsumer
from lib import urlfinder
import json


class UrlfinderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        req = json.loads(text_data)
        query = req['query']
        if query:
            any_success = False
            await self.send(text_data=json.dumps({'log': f'Query: {query}'}))
            async for url_scheme, response in urlfinder.test_urls(query):
                if response is None:
                    await self.send(text_data=json.dumps(
                        {'result': {'query': query, 'label': f'{url_scheme.label} (unknown error)', 'url': url_scheme.display_url()}}))
                    continue
                success = url_scheme.is_valid_response(response)
                if success:
                    await self.send(text_data=json.dumps(
                        {'result': {'query': query, 'label': url_scheme.label, 'url': url_scheme.display_url()}}))
                    any_success = True
                success_txt = 'success' if success else 'failure'
                await self.send(text_data=json.dumps(
                    {'log': f'{success_txt}: {url_scheme.label} {response.status_code} {url_scheme.display_url()}'}))
            if not any_success:
                await self.send(text_data=json.dumps({'control': {'code': 'nothing', 'query': query}}))
        await self.send(text_data=json.dumps({'log': 'done.', 'control': {'code': 'done', 'query': query}}))
