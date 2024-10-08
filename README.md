# chatter-bot
A bot that posts random predefined statuses on Mastodon, and also replies to mentions with random, predefined statuses.

First, do the pip!

```
pip install mastodon.py
```

Then, put the script onto your server!

```
nano path/to/script/chatter-bot.py
```

Don't forget to also crreate the statuses and replies!

```
nano path/to/script/statuses.json
```

```
nano path/to/script/replies.json
```

Then, schedule it! This is not a bot that is running at all times, so statues and replies will go out *only* when it runs (to conserve resources, we don't need a bot that's up and running at all times).

```
chmod +x path/to/script/chatter-bot.py
```

```
crontab -e
```

```
*/15 * * * * /path/to/your/virtualenv/bin/python /path/to/chatter-bot/chatter-bot.py
```

Set to run every 15 minutes, and to use a virtual environment (I prefer to do this cause it's easier to use pip that way, and there's less margin for error).

You're finished!

See it running in action, [here](https://mkultra.monster/@net_run).
