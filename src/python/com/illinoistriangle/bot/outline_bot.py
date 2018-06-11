import logging
import os
import time
import json

from slackclient import SlackClient
from com.illinoistriangle.lib.urlmarker import find_urls

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Bot User OAuth Access Tokenfrom https://api.slack.com/apps/AB1GJ5QLX/oauth?
bot = SlackClient(os.environ["BOT_OAUTH_TOKEN"])
user = SlackClient(os.environ["USER_OAUTH_TOKEN"])
allowed_channels = 'test_x',


#TODO get id from bot name
BOT_CALLOUT = '<@UAZUM5K33>'


def print_json(json_msg):
  """pretty pretty json"""
  logger.debug(json.dumps(json_msg, indent=4))


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
  if data['ok']:
    for item in data['channels']:
      if item['is_archived']:
        continue
      _channel_map[item['id']] = item
  else:
    logger.error("no channel found.")
  return _channel_map


channel_map = get_channels(bot)
allowed_channel_ids = [channel_id for channel_id in channel_map if channel_map[channel_id]['name'] in allowed_channels]

# This is the entry point for aws lambda execution.
def lambda_handler(data, context):
  """Handle an incoming HTTP request from a Slack chat-bot.
  """

  print(data)
  if "challenge" in data:
    return data["challenge"]

  # Grab the Slack event data.
  slack_event = data['event']

  handle_event(slack_event)


def search_thread_parent_for_urls(channel, thread_ts):
  """return list of urls from thread's parent post"""
  #TODO enable scope channels:history
  response = user.api_call(
              'channels.replies',
              channel=channel,
              thread_ts=thread_ts,
              )

  print_json(response)

  urls = []
  if response['ok'] and 'messages' in response:
    # from all thread messages, find earliest ts and return the text of that post
    parent_thread_text = response['messages'][0]['text']

    urls.extend(find_urls(parent_thread_text))

  return urls


def event_is_human_thread_reply(event):
  """return True if the event warrants the bot's response"""

  # if a message was posted...
  if 'type' in event and event['type'] == 'message':
    # ... by someone other than a bot...
    if 'subtype' not in event or event['subtype'] != 'bot_message':
      # ... in a thread...
      if 'thread_ts' in event:
        # TODO add channel whitelist
        # ... in an appropriate channel...
        if 'channel' in event and event['channel'] in ['C7RLA5HAA', ]:
          # ... and the bot was called...
          if 'text' in event and BOT_CALLOUT in event['text']:
            return True

  return False


def handle_event(event):
  # only reply to thread messages, made by humans, that call out the bot
  if event_is_human_thread_reply(event):

    # get list of urls from thread parent post
    urls = search_thread_parent_for_urls(event['channel'], event['thread_ts'])

    #TODO put url whitelist/blacklist test here.  urls should be filtered at this exact point.
    # if urls parsed successfully, post link
    if urls:
      logger.info("urls: {}".format(urls))
      outline_urls = ['<https://outline.com/{}|{}...>'.format(u, u[:30]) for u in urls]
      bot_text = '\r\n'.join(outline_urls)

    # if failure, apologize
    else:
      bot_text = "Sorry, but I couldn't find any urls to post.   :feelsbadman:"

    # always reply if event_is_human_thread_reply(event) = True
    bot.api_call(
      'chat.postMessage',
      channel=event['channel'],
      thread_ts=event['thread_ts'],
      unfurl_links='false',
      text=bot_text
      )

# This is the entry point for testing from command line
if __name__ == "__main__":

  if bot.rtm_connect():

    while bot.server.connected is True:
      events = bot.rtm_read()
      for evt in events:
        print_json(evt)
        handle_event(evt)

      time.sleep(1)
  else:
    logger.error("Connection Failed")
