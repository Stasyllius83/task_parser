import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
from bs4 import BeautifulSoup
import requests
import telebot


TELEGRAM_TOKEN = DATABASE = os.getenv('TELEGRAM_TOKEN')

TASK_TOPIC = ['brute', 'math','strings', 'greedy', \
              'implementation', 'sortings', 'constructive', \
                'algorithms', 'graph', 'matchings', 'shortest', 'paths', \
                    'Function', 'Problem', 'structures', 'hashing', 'search', \
                        'binary', 'number', 'theory', 'dp', 'pointers', \
                            'parsing', 'expression', 'two', '*special', 'data', 'bitmasks']

async def task_parser():

    num_of_page = 95
    for i in range(num_of_page):
        url = 'https://codeforces.com/problemset/page/' + str(i) + '?order=BY_SOLVED_DESC'
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page, 'lxml')

        all_tasks = []

        for a in soup.find_all('tr')[1:-1]:

            task_items = []

            line = ' '.join(a.text.split())
            line_words = line.split(' ', 1)
            words_in_line = line_words[1].split()

            list_word = []

            for word in words_in_line:
                res_word = word.replace(",","")
                if res_word not in TASK_TOPIC:
                    list_word.append(res_word)
                else:
                    break

            name = ' '.join(list_word)
            task_items.append(f'{name} № {line_words[0]}')

            for word in words_in_line:
                res_word = word.replace(",","")
                if res_word in TASK_TOPIC:
                    topic = res_word
                    break

            for word in words_in_line[-2:-1]:
                difficulty = word
                break

            for word in words_in_line[-1:]:
                quantity_solved = word[1:]
                break

            task_items.append(topic)
            task_items.append(difficulty)
            task_items.append(quantity_solved)
            all_tasks.append(task_items)

        return all_tasks



async def telegram_bot():
    req_data = []

    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(content_types=['text'])
    def start(message):
        if message.text == "Привет":
            bot.send_message(message.from_user.id, "Привет, напиши тему,чтоб я \
                              тебе прислал подборку на 10 задач? \
                             Список тем: brute, math, strings, greedy, \
                             implementation,  sortings, constructive, \
                             algorithms, graph, matchings, shortest, paths, \
                             Function, Problem, structures, hashing, search, binary, number, theory, dp, pointers, parsing, expression, two, *special, data, bitmasks")
            bot.register_next_step_handler(message, get_topic)

        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши Привет")
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


    def get_topic(message):
        global_topic = message.text
        bot.send_message(message.from_user.id, "Напиши уровень сложности?")
        bot.register_next_step_handler(message, get_difficulty)
        return global_topic


    def get_difficulty(message):
        global_difficulty = int(message.text)
        return global_difficulty


    bot.polling(non_stop=True, interval=0)

    return req_data.append(get_topic)



async def send_telegram(data):
    tsk = data.result()

    for item in tsk:
        print(item)
    save_data = tsk

    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(content_types=['text'])
    def send(message):
        if item != 0 and item != save_data:
            bot.send_message(message.from_user.id, item)


    bot.polling(non_stop=True, interval=0)
