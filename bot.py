import os
import slack_sdk
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Request, Response
from slackeventsapi import SlackEventAdapter
import re

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
            os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack_sdk.WebClient(token=os.environ['SLACK_API_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

welcome_messages = {}

class WelcomeMessage:
    START_TEXT = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":tada: WOW a demo was scheduled!!! :tada: \n\n *That means you will have to do some push-ups!* :wink:"
        }
    }

    DIVIDER = {
        "type": "divider"
    }

    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.timestamp = ''
        self.completed = False

    def get_message(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "blocks": [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }

    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_small_square:'

        text = f"{checkmark} *Go Go Go! You have to do 10 push-ups :muscle:*"

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

def send_message(channel, user):
    welcome = WelcomeMessage(channel, user)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestamp = response['ts']

    if channel not in welcome_messages:
        welcome_messages[channel] = {}
    welcome_messages[channel][user] = welcome


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    pattern = "gong"

    if user_id != None and BOT_ID != user_id and re.search(pattern, text, re.IGNORECASE):
        send_message(f'@{user_id}', user_id)

if __name__ == "__main__":
    app.run(debug=True)
