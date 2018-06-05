# Outline Bot

## Related files
```
bot/
lib/
```

## Prep (recommend doing so in a virtualenv)
```
pip install slackclient
```

## Run the code
```
BOT_TOKEN=... PYTHONPATH=$(pwd):$PYTHONPATH python bot/outline_bot.py
```

`BOT_TOKEN` is `OAuth Access Token` on https://api.slack.com/apps/AB1GJ5QLX/install-on-team?