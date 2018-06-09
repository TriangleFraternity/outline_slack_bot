# Outline Bot

## Related files

## Setup
Bootstrap Pants (the build tool)
```
./pants goals
```

## Run locally in RTM mode
For local runs the token is
`Bot User OAuth Access Token` from https://api.slack.com/apps/AB1GJ5QLX/oauth?
```
OAUTH_TOKEN=<token> ./pants run src/python/com/illinoistriangle/bot:bot
```
Local runs are in RTM mode. https://api.slack.com/rtm

## Deployment
`OAUTH_TOKEN` is `OAuth Access Token` on https://api.slack.com/apps/AB1GJ5QLX/install-on-team?

Deployment uses the events subscription. https://api.slack.com/events-api