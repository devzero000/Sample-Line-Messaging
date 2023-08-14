import firebase_admin
from apscheduler.schedulers.background import BackgroundScheduler
from firebase_admin import credentials
from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import config.settings as settings
import utils.functions as func
import utils.tasks as task

app = Flask(__name__)

base_api = '/api'

configuration = Configuration(access_token=settings.CHANNEL_ACCESS)
handler = WebhookHandler(settings.CHANNEL_SECRET)


@app.route(f'/', methods=['GET'])
def home():
    return {
        'message': "Hello! I'm Kernel, your stock technical information assistant.",
        'created': 'Nick Tinnapat',
    }


@app.route(f'{base_api}/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # You can read more type message event
    # source: # source: https://saixiii.com/chapter6-line-python-sdk/
    flex_content = func.generate_corousel_content()
    func.push_message(event, flex_content)


if __name__ == "__main__":
    # schedule tasks
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=task.task_set_keep_alive_web_server, trigger="interval", seconds=60)
    scheduler.add_job(func=task.task_alert_trade, trigger="interval", seconds=60)
    scheduler.start()

    # Init firebase
    cred = credentials.Certificate('config/credential.json')
    firebase_admin.initialize_app(cred)

    app.run(debug=False, port=8000)
