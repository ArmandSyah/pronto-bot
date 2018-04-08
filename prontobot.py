import os
import pprint
import time
from slackclient import SlackClient
from parseutils import parse_direct_mention
from commands import handle_command


pp = pprint.PrettyPrinter(indent=4)
slack_client = SlackClient(os.environ.get('PRONTO_BOT_TOKEN'))
prontobot_id = None

# constants
RTM_READ_DELAY = 1  # 1 seconds delay between reading from the RTM


def find_bot_commands(slack_events):
    message, channel, messaged_user_id = None, None, None
    bot_user_id = None
    for event in slack_events:
        pp.pprint(event)
        if event["type"] == "message" and "bot_id" not in event:
            channel = event["channel"]
            messaged_user_id = event["user"]
            bot_user_id, message = parse_direct_mention(event['text'])
    return (message, channel, messaged_user_id) if bot_user_id == prontobot_id else (None, None, None)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("ProntoBot is online!")
        prontobot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user_id = find_bot_commands(
                slack_client.rtm_read())
            if command:
                handle_command(slack_client, command, channel, user_id)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
