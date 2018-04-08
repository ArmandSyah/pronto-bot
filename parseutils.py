import re

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
QUESTION_REGEX = r"\[.*\]"
ANSWER_REGEX = r"\(.*\)"


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
