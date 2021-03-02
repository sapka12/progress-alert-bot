import os
import rollbar

from flask import Flask, request
from pymessenger2.bot import Bot
from tools.config import Config
from tools.options import Options
from tools.mongo_crud import MongoCrud
from tools.chart import Chart

rollbar.init(Config.ROLLBAR, 'production')

app = Flask(__name__)
bot = Bot(Config.ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    try:
        if request.method == 'GET':
            """Before allowing people to message your bot, Facebook has implemented a verify token
            that confirms all requests that your bot receives came from Facebook."""
            token_sent = request.args.get("hub.verify_token")
            return verify_fb_token(token_sent)
        else:
            output = request.get_json()
            for event in output['entry']:
                messaging = event['messaging']
                for message in messaging:
                    if message.get('message'):
                        recipient_id = message['sender']['id']
                        if message['message'].get('text'):
                            msg = message['message'].get('text')

                            rollbar.report_message("message received[{}]: {}".format(recipient_id, msg), "info")
                            opt = Options(MongoCrud(), Chart())
                            fb_responses = opt.answer_message(recipient_id, msg)
                            for response_sent_text in fb_responses:
                                send_message(opt, recipient_id, response_sent_text)
        return "Message Processed"
    except:
        rollbar.report_exc_info()


def verify_fb_token(token_sent):
    try:
        if token_sent == Config.VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return 'Invalid verification token'
    except:
        rollbar.report_exc_info()


def send_message(opt, recipient_id, response):
    try:
        if response.startswith(opt.IMAGE_PREFIX):
            image_path = response[len(opt.IMAGE_PREFIX):]
            rollbar.report_message("bot.send_image", recipient_id, image_path)
            bot.send_image(recipient_id, image_path)
        else:
            bot.send_text_message(recipient_id, response)

        return "success"
    except:
        rollbar.report_exc_info()


if __name__ == "__main__":

    app.run()
