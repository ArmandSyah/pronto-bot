import parseutils
from questions import questions

COMMAND_LIST = ["hello", "question", "add"]
DEFAULT_RESPONSE = "Not sure what you mean. Try *{}*.".format(
    ', '.join(str(x) for x in COMMAND_LIST))


def find_answer(question_text):
    question_obj = [q for q in questions if q['question']
                    == question_text]
    answer = None
    if question_obj:
        answer = question_obj[0]["answer"]
    return answer


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


def handle_command(slack_client, command, channel, user_id):
    response = None
    if command.startswith(COMMAND_LIST[0]):
        response = "Why, hello to you too!"
    elif command.startswith(COMMAND_LIST[1]):
        question_text = parseutils.parse_question(command)
        response = find_answer(question_text)
    elif command.startswith(COMMAND_LIST[2]):
        question, answer = parseutils.parse_question_answer(command)
        response = validate_question_answer(question, answer)

    if not user_id:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or DEFAULT_RESPONSE
        )
        return

    user_info = slack_client.api_call("users.info", user=user_id)
    new_channel_id = slack_client.api_call(
        "im.open", user=user_id)["channel"]["id"]
    response = f'{response or DEFAULT_RESPONSE} @{user_info["user"]["name"]}'
    slack_client.api_call("chat.postMessage", link_names=1,
                          channel=new_channel_id, text=response or DEFAULT_RESPONSE)
