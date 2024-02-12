import time
import random
import logging
import requests
import threading
import fake_useragent
from flask import Flask


class PingServer:
    def __init__(self, url: str, port: int = 80):
        self.url = url
        self.port = port

    def run(self):
        app = Flask('')

        @app.route('/')
        def home():
            return ':D'

        thread = threading.Thread(target=lambda: app.run(host=self.url, port=self.port))
        thread.start()


class PingClient:
    def __init__(self, url: str, port: int = 80, timeout_range: tuple[int, int] = (10, 25), allow_logs: bool = True):
        self.url = url
        self.port = port
        self.timeout_range = timeout_range
        self.useragent = fake_useragent.UserAgent()
        self.allow_logs = allow_logs

    def run(self):
        time.sleep(3)

        def auto_ping():
            while True:
                headers = {'user-agent': self.useragent.random}
                timeout = random.randint(*self.timeout_range)

                try:
                    res = requests.get(f'{self.url}:{self.port}', headers=headers, timeout=0.1)
                    status_code = res.status_code
                except requests.exceptions.ReadTimeout:
                    status_code = 'timed out'

                if self.allow_logs:
                    logging.info(f'Pinged {self.url}:{self.port} with a response: {status_code}. Timeout: {timeout}')
                time.sleep(timeout)

        auto_ping_thread = threading.Thread(target=auto_ping)
        auto_ping_thread.start()
