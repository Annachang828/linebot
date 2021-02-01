from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('OXYuMcnFWsFC0Z4XUpZ5t5VQ/Coo5enLnZ8D8ppYUfmGxIUEgrm9prlIN0jj3JZcHEPpfWtMFfKEAQeJTFmQex2OA+6D5S2ygrV5O80caXhyMHfGNXU6T8ks5YupBnr82+jF1k+Ky9lns+CmAdj0VwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('01c89c596359d202cc965425b8c5851b')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂~~~'
    
    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', 'Hi', '嗨']:
        r = 'hi'
    elif msg == '你吃飯了嗎':
        r = 'Not yet'
    elif msg == '你是誰?':
        r = '我是機器人!'
    elif '聊' in msg:
        r = '你想要找人聊天嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()