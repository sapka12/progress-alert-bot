from flask import Flask, request
from pymessenger2.bot import Bot
import os
from options import answer_message, IMAGE_PREFIX

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def receive_message():
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
                        print("message received:", msg)
                        # fb_responses = answer_message(recipient_id, msg)
                        # for response_sent_text in fb_responses:
                        #     send_message(recipient_id, response_sent_text)
    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_message(recipient_id, response):
    if response.startswith(IMAGE_PREFIX):
        bot.send_image(recipient_id, response[len(IMAGE_PREFIX):])
    else:
        bot.send_text_message(recipient_id, response)

    return "success"


if __name__ == "__main__":
    app.run()
