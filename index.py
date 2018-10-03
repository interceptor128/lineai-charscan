import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(6jwapyUVgjIBRYLDIRgHl1cLJQBwPxYGW+zAp+ylMk13bKZVQDCVflTQdSwJgSn8vKV7gx6HPttAjsebvDtLQzcfyP7udhRdWQLW9y3++yvVeigtz6r8/uFh38zwBb61Reaf39WG1uypLDtRttvYfAdB04t89/1O/w1cDnyilFU=)
handler = WebhookHandler(40b2d4da4e99a79abd3418a61ab3cf61)

@app.route("/callback", methods=['POST'])
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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )