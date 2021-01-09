import os
import requests


class Notify:
    def __init__(self):
        self.SCKEY = os.environ.get('SCKEY')

    def send(self, title, content):
        if self.SCKEY:
            requests.get(f'https://sc.ftqq.com/{self.SCKEY}.send', params={
                'text': title,
                'desp': content
            })
