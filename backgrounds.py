import random
import time

import requests
from flask import Flask
from threading import Thread
import logging

log = logging.getLogger('logger')
log.setLevel(logging.ERROR)
app = Flask('')


def auto_ping():
    time.sleep(15)

    while True:
        time.sleep(60)
        requests.get('http://127.0.0.1:80')


@app.route('/')
def home():
    return ':D'


def start_keeping():
    thread = Thread(target=lambda: app.run(host='0.0.0.0', port=80))
    thread.start()

    thread_auto_ping = Thread(target=lambda: auto_ping())
    thread_auto_ping.start()
