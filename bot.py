import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Request, Response
from slackeventsapi import SlackEventAdapter
import string
from datetime import datetime, timedelta
import time
import re

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
            os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    pattern = "get out"

    if BOT_ID != user_id and re.search(pattern, text, re.IGNORECASE):
        client.chat_postMessage(channel=channel_id, text='yes! get me out of here')


if __name__ == "__main__":
    app.run(debug=True)
