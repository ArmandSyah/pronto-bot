# ProntoBot

This is ProntoBot, he's going to do great things, I guarantee it!

## Tools we need:
- Python3.6
- Pip 3
- VirtualEnv
- Free slack account and a workspace with it

[Follow this guide here](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) to find out how to get and set up the proper authentication tokens for this bot

To make this work follow these steps:

## Downloading the bot
- Install Python 3.6 and Pip3
- Install VirtualEnv (**pip3 install virtualenv**) 
- Install your virtualenv (**virtualenv -p python3 venv**)
- Activate your virtual environment by doing this command(**source venv/bin/activate** on mac/linux **venv\Scripts\activate.bat** on windows) 
- Install the requirements (**pip install -r requirements.txt**)
- Finally, run the bot (**python prontobot.py**)

## List of Avaiable commands
- **hello** (aliases: h, hi): Pronto says hi back! *Usage: @{botname} hello*
- **question** (aliases: q): Ask Pronto a question *Usage: @{botname} question [What day is it today]*
- **add_question** (aliases: add, a): If Pronto doesn't know the answer to the question, just tell him the answer to one and he'll remember 
 *@{botname} add_question [When's my birthday] (January 17th)*
- **list_questions** (aliases: list): Pronto will tell you every question you can ask it at the time *Usage @{botname} list_questions*