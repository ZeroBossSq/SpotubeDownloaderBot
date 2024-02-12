import time
import random
import logging
from threading import Thread
import requests
import fake_useragent
from flask import Flask

logger = logging.getLogger('logger')
logger.setLevel(logging.ERROR)
useragent = fake_useragent.UserAgent()
app = Flask('')


def auto_ping():
    while True:
        headers = {'user-agent': useragent.random}

        time.sleep(random.randint(10, 25))
        requests.get('http://0.0.0.0:80', headers=headers)


@app.route('/')
def home():
    return ':D'


def start_keeping():
    thread = Thread(target=lambda: app.run(host='0.0.0.0', port=80))
    thread.start()
    thread_auto_ping = Thread(target=lambda: auto_ping())
    thread_auto_ping.start()
