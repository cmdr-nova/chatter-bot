import json
import random
from mastodon import Mastodon

# Needs full path when using a cronjob
REPLIED_MENTIONS_FILE = 'path/to/replied/replied_mentions.json'

# Load replied mentions from file
def load_replied_mentions(file_path):
    try:
        with open(file_path, 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

# Save replied mentions to file
def save_replied_mentions(file_path, replied_mentions):
    with open(file_path, 'w') as file:
        json.dump(list(replied_mentions), file)

# Load statuses from file
def load_statuses(file_path):
    try:
        print(f"Loading statuses from: {file_path}")  # Debug print
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"Raw data loaded: {data}")  # Debug print
            if isinstance(data, dict) and "statuses" in data:
                statuses = data["statuses"]
            elif isinstance(data, list):
                statuses = data
            else:
                statuses = []
            print(f"Loaded statuses: {statuses}")  # Debug print
            return statuses
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Debug print
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")  # Debug print
        return []

# Load replies from file
def load_replies(file_path):
    try:
        print(f"Loading replies from: {file_path}")  # Debug print
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"Raw data loaded: {data}")  # Debug print
            if isinstance(data, dict) and "replies" in data:
                replies = data["replies"]
            elif isinstance(data, list):
                replies = data
            else:
                replies = []
            print(f"Loaded replies: {replies}")  # Debug print
            return replies
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Debug print
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")  # Debug print
        return []

# Post a random status to Mastodon with a spoiler warning
def post_random_status(mastodon_client, statuses):
    if statuses:
        status = random.choice(statuses)
        spoiler_text = "Automated bot poasting"
        mastodon_client.status_post(status=status, spoiler_text=spoiler_text)
        print(f"Posted status with spoiler warning: {status}")
    else:
        print("No statuses available to post.")

# Reply to mentions with a random reply
def reply_to_mentions(mastodon_client, replies, replied_mentions):
    mentions = mastodon_client.notifications(mentions_only=True)
    for mention in mentions:
        if mention['type'] == 'mention':
            status_id = mention['status']['id']
            account = mention['account']['acct']
            
            # Check if the bot has already replied to this mention
            if status_id not in replied_mentions:
                reply = random.choice(replies)
                reply_status = f"@{account} {reply}"
                mastodon_client.status_post(status=reply_status, in_reply_to_id=status_id)
                print(f"Replied to @{account} with: {reply}")
                
                # Record the mention as replied, so that it never does so ever again, even if you have automated post deletion turned on
                replied_mentions.add(status_id)

if __name__ == "__main__":
    # Put your access token from Mastodon here
    ACCESS_TOKEN = 'your_access_token'
    INSTANCE_URL = 'https://your.instance'

    # Set us up the Mastodon client
    mastodon_client = Mastodon(
        access_token=ACCESS_TOKEN,
        api_base_url=INSTANCE_URL
    )

    # Load statuses and replies from JSON files
    statuses_file_path = 'path/to/statuses.json'
    replies_file_path = 'path/to/replies.json'
    statuses = load_statuses(statuses_file_path)
    replies = load_replies(replies_file_path)

    # Load replied mentions
    replied_mentions = load_replied_mentions(REPLIED_MENTIONS_FILE)

    # Post a random status
    post_random_status(mastodon_client, statuses)

    # Reply to mentions
    reply_to_mentions(mastodon_client, replies, replied_mentions)

    # Save replied mentions
    save_replied_mentions(REPLIED_MENTIONS_FILE, replied_mentions)
