import time

from slackclient import SlackClient
from urlextract import URLExtract

from secrets import slack_api_token

extractor = URLExtract()

sc = SlackClient(slack_api_token)

FIELD_TEXT = 'text'
FIELD_CHANNEL = 'channel'
VALUE_TYPE_BOT_MESSAGE = 'bot_message'
VALUE_TYPE_MESSAGE = 'message'
APP_NAME = ''

if sc.rtm_connect():
  while sc.server.connected is True:
    events = sc.rtm_read()
    if events:
      for e in events:
        if 'subtype' in e and e['subtype'] == VALUE_TYPE_BOT_MESSAGE:
          continue

        if e['type'] != VALUE_TYPE_MESSAGE:
          continue

        if FIELD_TEXT not in e:
          continue

        urls = extractor.find_urls(e[FIELD_TEXT])
        print("event:", events)
        print("urls", urls)
        outline_urls = ['https://outline.com/' + u for u in urls]
        sc.api_call(
          "chat.postMessage",
          # TODO: param this.
          channel=e[FIELD_CHANNEL],
          text=' '.join(outline_urls)
        )

    time.sleep(1)
else:
  print("Connection Failed")
