import time
import calendar
from datetime import date, datetime

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
