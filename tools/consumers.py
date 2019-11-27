from channels.generic.websocket import WebsocketConsumer
from lib import urlfinder
import json


class UrlfinderConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        req = json.loads(text_data)
        query = req['query']
        if query:
            self.send(text_data=json.dumps({'log': f'Query: {query}'}))
            for label, url, code in urlfinder.test_urls(query):
                self.send(text_data=json.dumps({'log': f'{label}: {code} {url}'}))
        self.send(text_data=json.dumps({'log': 'done.'}))
