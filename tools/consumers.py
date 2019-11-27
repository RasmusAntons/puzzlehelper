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
            await self.send(text_data=json.dumps({'log': f'Query: {query}'}))
            async for url_scheme, response in urlfinder.test_urls(query):
                success = url_scheme.is_valid_response(response)
                if success:
                    await self.send(text_data=json.dumps({'result': {'label': url_scheme.label, 'url': url_scheme.display_url()}}))
                success_txt = 'success' if success else 'failure'
                await self.send(text_data=json.dumps({'log': f'{success_txt}: {url_scheme.label} {response.status_code} {url_scheme.display_url()}'}))
        await self.send(text_data=json.dumps({'log': 'done.'}))
