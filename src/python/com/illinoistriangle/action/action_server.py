import json

import requests
from flask import Flask, request

from com.illinoistriangle.lib.urlmarker import find_urls

app = Flask(__name__)


@app.route('/action', methods=['GET', 'POST'])
def flask_handle():
  payload = json.loads(request.form['payload'])
  app.logger.debug(payload)

  handle_payload(payload)
  app.logger.debug(r.status_code)
  return 'Hello, World!'


def handle_payload(payload):
  response_url = payload['response_url']
  trigger_user = payload['user']['name']
  text = payload['message']['text']
  urls = find_urls(text)
  if urls:
    outline_urls = ['<https://outline.com/{}|{}...>'.format(u, u[:30]) for u in urls]
    response_text = "Per @{}'s request, here are the outline urls: {}".format(trigger_user, ' '.join(outline_urls))
    response_type = 'in_channel'
  else:
    response_text = 'No url found.'
    response_type = 'ephemeral'
  reply_data = {
    "text": response_text,
    "response_type": response_type
  }
  requests.post(response_url, json=reply_data)


# This is the entry point for aws lambda execution.
def lambda_handler(data, context):
  """Handle an incoming HTTP request from a Slack chat-bot.
  """

  print(data)
  if "challenge" in data:
    return data["challenge"]

  handle_payload(json.loads(data))


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=80)
