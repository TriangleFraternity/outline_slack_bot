import logging
import os
import time

from slackclient import SlackClient

from lib.urlmarker import find_urls

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sc = SlackClient(os.environ["BOT_TOKEN"])

FIELD_TEXT = 'text'
FIELD_CHANNEL = 'channel'
VALUE_TYPE_BOT_MESSAGE = 'bot_message'
VALUE_TYPE_MESSAGE = 'message'
APP_NAME = ''


def get_channels(client):
  """
  Example data:
    {'ok': True, 'channels': [
    {'id': 'C2RN38ES1', 'name': '2016_bboc_draft', 'is_channel': True, 'created': 1476928957, 'is_archived': True,
     'is_general': False, 'unlinked': 0, 'creator': 'U0JT5B8B0', 'name_normalized': '2016_bboc_draft', 'is_shared': False,
     'is_org_shared': False, 'is_member': False, 'is_private': False, 'is_mpim': False, 'members': [],
     'topic': {'value': 'Dick Length Contest', 'creator': 'U0HC7NH8W', 'last_set': 1476929171},
     'purpose': {'value': 'Drafting Beer Buddies?', 'creator': 'U0JT5B8B0', 'last_set': 1476928957}, 'previous_names': [],
     'num_members': 0},
    {'id': 'C7206G0ET', 'name': 'academics', 'is_channel': True, 'created': 1505085766, 'is_archived': False,
     'is_general': False, 'unlinked': 0, 'creator': 'U22SKHXKL', 'name_normalized': 'academics', 'is_shared': False,
     'is_org_shared': False, 'is_member': False, 'is_private': False, 'is_mpim': False, 'members': [],
     'topic': {'value': '', 'creator': 'U22SKHXKL', 'last_set': 1505085885},
     'purpose': {'value': 'To learn you something new ', 'creator': 'U22SKHXKL', 'last_set': 1505085885},
     'previous_names': [], 'num_members': 35},
   }

  :param client:
  :return: channel info by id
  """

  data = client.api_call("channels.list")
  _channel_map = {}
  if 'ok' in data:
    for item in data['channels']:
      if item['is_archived']:
        continue
      _channel_map[item['id']] = item
  else:
    logger.error("no channel found.")
  return _channel_map


channel_map = get_channels(sc)


def lambda_handler(data, context):
  """Handle an incoming HTTP request from a Slack chat-bot.
  """

  print(data)
  if "challenge" in data:
    return data["challenge"]

  # Grab the Slack event data.
  slack_event = data['event']

  handle_event(slack_event)


def handle_event(e):
  if 'subtype' in e and e['subtype'] == VALUE_TYPE_BOT_MESSAGE:
    return

  if e['type'] != VALUE_TYPE_MESSAGE:
    return

  if FIELD_TEXT not in e:
    return

  channel_id = e[FIELD_CHANNEL]
  if channel_id not in channel_map:
    return

  if channel_map[channel_id]['name'] not in ['politics', 'test_x']:
    return
  urls = find_urls(e[FIELD_TEXT])
  logger.info("urls: {}".format(urls))
  outline_urls = ['https://outline.com/' + u for u in urls]
  sc.api_call(
    "chat.postMessage",
    # TODO: param this.
    channel=channel_id,
    text=' '.join(outline_urls)
  )


if __name__ == "__main__":
  if sc.rtm_connect():
    while sc.server.connected is True:
      events = sc.rtm_read()
      for evt in events:
        handle_event(evt)

      time.sleep(1)
  else:
    logger.error("Connection Failed")
