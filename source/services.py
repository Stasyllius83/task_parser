# import asyncio
# import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
from bs4 import BeautifulSoup
import requests
#import telebot



#URL = 'https://api.telegram.org/bot'
#TELEGRAM_TOKEN = DATABASE = os.getenv('TELEGRAM_TOKEN')
#bot = telebot.TeleBot(TELEGRAM_TOKEN)

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



# async def telegram_bot():



#     @bot.message_handler(content_types=['text'])
#     def start(message):
#         if message.text == "Привет":
#             bot.send_message(message.from_user.id, "Привет, напиши тему,чтоб я \
#                               тебе прислал подборку из 10 задач? \
#                              Список тем: brute, math, strings, greedy, \
#                              implementation,  sortings, constructive, \
#                              algorithms, graph, matchings, shortest, paths, \
#                              Function, Problem, structures, hashing, search, binary, number, theory, dp, pointers, parsing, expression, two, *special, data, bitmasks")
#             bot.register_next_step_handler(message, get_topic)

#         elif message.text == "/help":
#             bot.send_message(message.from_user.id, "Напиши Привет")
#         else:
#             bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


#     def get_topic(message):

#         global_topic = message.text
#         tsk.task_req(global_topic)
#         bot.send_message(message.from_user.id, "Напиши уровень сложности?")
#         bot.register_next_step_handler(message, get_difficulty)

#         return global_topic


#     def get_difficulty(message):

#         global_difficulty = int(message.text)

#         return global_difficulty


#     bot.polling(non_stop=True, interval=0)



# @bot.message_handler(content_types=['text'])
# def start(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, напиши тему,чтоб я \
#                               тебе прислал подборку из 10 задач? \
#                              Список тем: brute, math, strings, greedy, \
#                              implementation,  sortings, constructive, \
#                              algorithms, graph, matchings, shortest, paths, \
#                              Function, Problem, structures, hashing, search, binary, number, theory, dp, pointers, parsing, expression, two, *special, data, bitmasks")
#         bot.register_next_step_handler(message, get_topic)

#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши Привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


# def get_topic(message):

#     global_topic = message.text

#     bot.send_message(message.from_user.id, "Напиши уровень сложности?")
#     bot.register_next_step_handler(message, get_difficulty)

#     return global_topic


# def get_difficulty(message):

#     global_difficulty = int(message.text)

#     return global_difficulty






# async def send_telegram():
#     # tsk = data.result()

#     # for item in tsk:
#     #     print(item)
#     # save_data = tsk

#     bot = telebot.TeleBot(TELEGRAM_TOKEN)

#     @bot.message_handler(content_types=['text'])
#     def send(message):
#         if item != 0 and item != save_data:
#             bot.send_message(message.from_user.id, item)


#     bot.polling(non_stop=True, interval=0)



# def get_updates(offset=0):
#     result = requests.get(f'{URL}{TELEGRAM_TOKEN}/getUpdates?offset={offset}').json()
#     return result['result']

# def send_message(chat_id, text):
#     requests.get(f'{URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

# def check_message(chat_id, message):
#     for mes in message.lower().replace(',', '').split():
#         if mes in ['привет',]:
#             send_message(chat_id, "Привет, напиши тему,чтоб я \
#                               тебе прислал подборку из 10 задач? \
#                              Список тем: brute, math, strings, greedy, \
#                              implementation,  sortings, constructive, \
#                              algorithms, graph, matchings, shortest, paths, \
#                              Function, Problem, structures, hashing, search, \
#                          binary, number, theory, dp, pointers, parsing, \
#                          expression, two, *special, data, bitmasks")
#         # if mes in ['дела?', 'успехи?']:
#         #     send_message(chat_id, 'Спасибо, хорошо!')

# def run_telegram():
#     update_id = get_updates()[-1]['update_id'] # Присваиваем ID последнего отправленного сообщения боту
#     while True:
#         time.sleep(2)
#         messages = get_updates(update_id) # Получаем обновления
#         for message in messages:
#             # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
#             if update_id < message['update_id']:
#                 update_id = message['update_id'] # Присваиваем ID последнего отправленного сообщения боту
#                 # Отвечаем тому кто прислал сообщение боту
#                 check_message(message['message']['chat']['id'], message['message']['text'])
#             elif message in TASK_TOPIC:
#                 return message
