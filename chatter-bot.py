import json
import random
import os
from mastodon import Mastodon

# mastodon credentials
INSTANCE_URL = 'your_instance_url'
ACCESS_TOKEN = 'your_access_token'

# determine the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# path to the statuses.json and replies.json files
statuses_file_path = os.path.join(script_dir, 'statuses.json')
replies_file_path = os.path.join(script_dir, 'replies.json')

# load statuses from JSON file
def load_statuses(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['statuses']

# load replies from JSON file
def load_replies(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['replies']

# post a random status to Mastodon
def post_random_status(mastodon_client, statuses):
    status = random.choice(statuses)
    mastodon_client.status_post(status=status)
    print(f"Posted status: {status}")

# reply to mentions with a random reply
def reply_to_mentions(mastodon_client, replies):
    mentions = mastodon_client.notifications(mentions_only=True)
    for mention in mentions:
        if mention['type'] == 'mention':
            status_id = mention['status']['id']
            account = mention['account']['acct']
            
            # check if the bot has already replied to this mention
            if not mastodon_client.status_context(status_id)['descendants']:
                reply = random.choice(replies)
                reply_status = f"@{account} {reply}"
                mastodon_client.status_post(status=reply_status, in_reply_to_id=status_id)
                print(f"Replied to @{account} with: {reply}")

if __name__ == "__main__":
    # initialize Mastodon client
    mastodon_client = Mastodon(
        access_token=ACCESS_TOKEN,
        api_base_url=INSTANCE_URL
    )

    # load statuses and replies from JSON files
    statuses = load_statuses(statuses_file_path)
    replies = load_replies(replies_file_path)

    # post a random status
    post_random_status(mastodon_client, statuses)

    # reply to mentions
    reply_to_mentions(mastodon_client, replies)
