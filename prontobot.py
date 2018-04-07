import os
import time
import re
import pprint
import calendar
from slackclient import SlackClient
from datetime import date, datetime

pp = pprint.PrettyPrinter(indent=4)
slack_client = SlackClient(os.environ.get('PRONTO_BOT_TOKEN'))
prontobot_id = None

# constants
RTM_READ_DELAY = 1  # 1 seconds delay between reading from the RTM
COMMAND_LIST = ["hello", "question", "add"]
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
QUESTION_REGEX = r"\[.*\]"
ANSWER_REGEX = r"\(.*\)"

questions = [{"question": "What day is it today",
              "answer": f"Today is {calendar.day_name[date.today().weekday()]}!"},
             {"question": "What time is it right now",
                 "answer": f"{time.strftime('%H:%M', time.localtime())}"},
             {"question": "What's the name of this company", "answer": "ProntoForms!"},
             {"question": "Anime Recommendations",
              "answer": "*Sora Yori mo Tooi Basho* \n *K-On!* \n *Gurren Laggan* \n *Mob Psycho 100* \n *Ping Pong the Animation*"},
             {"question": "When are the tech talks at ProntoForms",
                 "answer": "Every thursday!"},
             {"question": "What is this",
                 "answer": "I'm a slack bot, designed to answer your questions, among other things if someone programs it"},
             {"question": "Who made you", "answer": "Armand did"},
             {"question": "Why were you made", "answer": "I was a hack day project"}]


def find_answer(question_text):
    question_obj = [q for q in questions if q['question']
                    == question_text]
    answer = None
    if question_obj:
        answer = question_obj[0]["answer"]
    return answer


def parse_bot_commands(slack_events):
    message, channel, messaged_user_id = None, None, None
    bot_user_id = None
    for event in slack_events:
        pp.pprint(event)
        if event["type"] == "message" and "bot_id" not in event:
            channel = event["channel"]
            messaged_user_id = event["user"]
            bot_user_id, message = parse_direct_mention(event['text'])
    return (message, channel, messaged_user_id) if bot_user_id == prontobot_id else (None, None, None)


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def parse_question(message_text):
    matches = re.search(QUESTION_REGEX, message_text)
    question_text = None
    if matches:
        question_text = matches.group(0).replace("[", "").replace("]", "")
    return question_text


def parse_answer(message_text):
    matches = re.search(ANSWER_REGEX, message_text)
    answer_text = None
    if matches:
        answer_text = matches.group(0).replace("(", "").replace(")", "")
    return answer_text


def parse_question_answer(message_text):
    question = parse_question(message_text)
    answer = parse_answer(message_text)
    return question, answer


def validate_question_answer(question, answer):
    response = None
    if question and answer:
        new_question_object = {"question": question, "answer": answer}
        questions.append(new_question_object)
        response = "Question has been added!"
    elif not question:
        response = "Question not found. Make sure you enclose your question with square brackets []"
    elif not answer:
        response = "Answer not found. Make sure you enclose your answer with brackets ()"
    return response


def handle_command(command, channel, user_id):
    default_response = "Not sure what you mean. Try *{}*.".format(
        ', '.join(str(x) for x in COMMAND_LIST))

    response = None
    if command.startswith(COMMAND_LIST[0]):
        response = "Why, hello to you too!"
    elif command.startswith(COMMAND_LIST[1]):
        question_text = parse_question(command)
        response = find_answer(question_text)
    elif command.startswith(COMMAND_LIST[2]):
        question, answer = parse_question_answer(command)
        response = validate_question_answer(question, answer)

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
