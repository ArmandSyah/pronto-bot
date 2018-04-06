import os
import time
import re
import pprint
import calendar
from slackclient import SlackClient
from datetime import date

pp = pprint.PrettyPrinter(indent=4)
slack_client = SlackClient(os.environ.get('PRONTO_BOT_TOKEN'))
prontobot_id = None

# constants
RTM_READ_DELAY = 1  # 1 seconds delay between reading from the RTM
COMMAND_LIST = ["hello", "question"]
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
QUESTION_REGEX = r"\[.*\]"

questions = [{"question": "What day is it today?",
              "answer": f"Today is {calendar.day_name[date.today().weekday()]}!"},
             {"question": "What's the name of this company?", "answer": "ProntoForms!"}]


def parse_bot_commands(slack_events):
    for event in slack_events:
        print(event)
        if event["type"] == "message" and "bot_id" not in event:
            channel = event["channel"]
            messaged_user_id = event["user"]
            bot_user_id, message = parse_direct_mention(event['text'])
            if bot_user_id == prontobot_id:
                return message, channel, messaged_user_id
    return None, None, None


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def parse_question(message_text):
    print(message_text, QUESTION_REGEX)
    matches = re.search(QUESTION_REGEX, message_text)
    if matches:
        question_text = matches.group(0).replace("[", "").replace("]", "")
        answer = [q for q in questions if q['question']
                  == question_text][0]['answer']
        return answer


def handle_command(command, channel, user_id):
    default_response = "Not sure what you mean. Try *{}*.".format(
        ', '.join(str(x) for x in COMMAND_LIST))

    response = None
    if command.startswith(COMMAND_LIST[0]):
        response = "Why, hello to you too!"
    elif command.startswith(COMMAND_LIST[1]):
        response = parse_question(command)

    if not user_id:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )
        return

    user_info = slack_client.api_call("users.info", user=user_id)
    new_channel_id = slack_client.api_call(
        "im.open", user=user_id)["channel"]["id"]
    response = f'{response or default_response} @{user_info["user"]["name"]}'
    slack_client.api_call("chat.postMessage", link_names=1,
                          channel=new_channel_id, text=response or default_response)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("ProntoBot is online!")
        prontobot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user_id = parse_bot_commands(
                slack_client.rtm_read())
            if command:
                handle_command(command, channel, user_id)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
