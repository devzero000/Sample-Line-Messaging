import requests
import config.api as api

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest, FlexMessage, FlexContainer,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import config.settings as settings
import utils.functions as func

app = Flask(__name__)

base_api = '/api'
keep_alive = 0


def set_keep_alive_web_server():
    requests.get(api.WEBSERVER)


scheduler = BackgroundScheduler()
scheduler.add_job(func=set_keep_alive_web_server, trigger="interval", seconds=60)
scheduler.start()

configuration = Configuration(access_token=settings.CHANNEL_ACCESS)
handler = WebhookHandler(settings.CHANNEL_SECRET)


@app.route(f'/', methods=['GET'])
def home():
    return {
        'message': "Hello! I'm Kernel, your stock technical information assistant.",
        'created': 'Nick Tinnapat',
        'keep-alive': keep_alive
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

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        """
        # If you want the system to handle messages that users type in, by detecting 
        # from the event message (received message), you can explore Dialogflow for further implementation.
        receive_text = event.message.text
        """

        flex_content = func.generate_corousel_content()
        message = FlexMessage(alt_text="OverTrade Signal", contents=FlexContainer.from_json(flex_content))
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[message]
            )
        )


if __name__ == "__main__":
    app.run(debug=False, port=8000)
