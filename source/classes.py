import copy
import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Numeric, UniqueConstraint
from source.services import task_parser
Base = declarative_base()
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
DATABASE = os.getenv('DB_CONNECT')

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage



class Task(Base):
    """Класс для формирования модели задачи в orm sqlalchemy

    Args:
        Base (_type_): _description_

    Returns:
        class 'type': _description_
    """
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column('topic', String)
    quantity_solved = Column('quantity_solved', Numeric)
    name_number = Column('name_number', String)
    difficulty = Column('difficulty', Numeric)
    UniqueConstraint('name_number', name='idx_name_number')

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Task_base:
    """Класс для работы с данными спарсенными с сайта https://codeforces.com/

    Returns:
        _type_: _description_
    """
    def __init__(self) -> None:
        """
        Инициализация класса. Инициализированны подключение к бд posgresql, сессия и имя таблицы
        """
        self.engine = create_engine(DATABASE)
        self.session = self.create_session(self.engine)
        self.create_table('task_parser')


    def create_table(self, table_name):
        """Метод для создания таблицы в бд

        Args:
            table_name (str): имя таблицы создаваемой в базе данных
        """
        if not self.engine.dialect.has_table(self.engine.connect(), table_name):
            Base.metadata.create_all(self.engine)


    @staticmethod
    def create_session(engine):
        """Статический метод для создания сессии

        Args:
            engine (_type_): _description_

        Returns:
            .__bases__: экземпляр сессии
        """
        Session = sessionmaker(bind=engine)
        return Session()


    def fill_db(self):
        """Метод для заполнения базы данных. Вызывает функцию парсера task_parser()
        """
        try:
            all_tasks = task_parser()

            for task in all_tasks:

                session = self.create_session(self.engine)

                task = Task(
                    topic=task[1],
                    quantity_solved=task[3],
                    name_number=task[0],
                    difficulty=task[2],
                )

                session.add(task)
                session.commit()
            session.close()

        except Exception as e:
            print(f"Произошла ошибка {e}")
            time.sleep(10)


    def task_req(self, topic, difficulty):
        """Метод берет из бд 10 задач по выбранным тематике и сложности

        Args:
            topic (str): тема задачи
            difficulty (str): сложность задачи

        Returns:
            list: список запрошенных задач
        """
        session = self.create_session(self.engine)

        tasks_req = session.query(Task).filter(Task.topic == topic, Task.difficulty == difficulty,).order_by(Task.id.desc()).limit(10).all()

        all_task_list = []
        for obj in tasks_req:
            task_list = []
            task_list.append(obj.name_number)
            task_list.append(obj.topic)
            task_list.append(int(obj.difficulty))
            task_list.append(int(obj.quantity_solved))
            all_task_list.append(task_list)
        return all_task_list


    def task_detail(self, name_N):
        """Метод достает из бд данные по имени и номеру задачи

        Args:
            name_N (str): название и номер задачи

        Returns:
            list: список деталей запрошенной задачи
        """
        session = self.create_session(self.engine)

        task_detail = session.query(Task).filter(Task.name_number.ilike(name_N)).limit(1).all()

        for obj in task_detail:
            task_detail_list = []
            task_detail_list.append(obj.name_number)
            task_detail_list.append(obj.topic)
            task_detail_list.append(int(obj.difficulty))
            task_detail_list.append(int(obj.quantity_solved))
            return task_detail_list


class Io_telebot:
    """Класс для работы с телеграм ботом
    """

    """Параметры для получения из телеграм бота
    """
    new_param = {
            'topic': 0,
            'difficulty': 0,
            'name_n': 0
        }

    TOKEN: str = os.getenv('TELEGRAM_TOKEN')

    def __init__(self):
        """Инициализация класса, списка задач, списка детализации задачи. Создание экземпляра класса задач.
        """
        self.task_base = Task_base()
        self.list_tasks = []
        self.task_detail = []
        self.param = copy.deepcopy(self.new_param)
        self.bot = Bot(self.TOKEN)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

    def __call__(self):
        """Метод __call__ вся логика бота
        """
        class Data_parse(StatesGroup):
            choosing_topic = State()
            choosing_difficulty = State()
            get_detail = State()

        but_1 = KeyboardButton('/Task_parser')
        keybut_1 = ReplyKeyboardMarkup(resize_keyboard=True)
        keybut_1.add(but_1)

        keybut_2 = ReplyKeyboardMarkup(resize_keyboard=True)
        # keybut_2 = InlineKeyboardMarkup(row_width=3)
        # keybut_2.add(InlineKeyboardButton(text='brute'), InlineKeyboardButton(text='math'), InlineKeyboardButton(text='strings'))
        but_2 = KeyboardButton('/brute')
        but_3 = KeyboardButton('/math')
        but_4 = KeyboardButton('/strings')
        but_5 = KeyboardButton('/greedy')
        but_6 = KeyboardButton('/implementation')
        but_7 = KeyboardButton('/sortings')
        but_8 = KeyboardButton('/constructive')
        but_9 = KeyboardButton('/algorithms')
        but_10 = KeyboardButton('/graph')
        but_11 = KeyboardButton('/matchings')
        but_12 = KeyboardButton('/shortest')
        but_13 = KeyboardButton('/paths')
        but_14 = KeyboardButton('/Function')
        but_15 = KeyboardButton('/Problem')
        but_16 = KeyboardButton('/structures')
        but_17 = KeyboardButton('/hashing')
        but_18 = KeyboardButton('/search')
        but_19 = KeyboardButton('/binary')
        but_20 = KeyboardButton('/number')
        but_21 = KeyboardButton('/theory')
        but_22 = KeyboardButton('/dp')
        but_23 = KeyboardButton('/pointers')
        but_24 = KeyboardButton('/parsing')
        but_25 = KeyboardButton('/expression')
        but_26 = KeyboardButton('/two')
        but_27 = KeyboardButton('/*special')
        but_28 = KeyboardButton('/data')
        but_29 = KeyboardButton('/bitmasks')
        keybut_2.add(but_2).add(but_3).add(but_4).add(but_5).add(but_6).add(but_7).add(but_8)\
            .add(but_9).add(but_10).add(but_11).add(but_12).add(but_13).add(but_14).add(but_15)\
                .add(but_16).add(but_17).add(but_18).add(but_19).add(but_20).add(but_21).add(but_22)\
                    .add(but_23).add(but_24).add(but_25).add(but_26).add(but_27).add(but_28).add(but_29)

        keybut_3 = ReplyKeyboardMarkup(resize_keyboard=True)
        but_30 = KeyboardButton('/800')
        but_31 = KeyboardButton('/900')
        but_32 = KeyboardButton('/1000')
        but_33 = KeyboardButton('/1100')
        but_34 = KeyboardButton('/1200')
        but_35 = KeyboardButton('/1300')

        keybut_3.add(but_30).add(but_31).add(but_32).add(but_33).add(but_34).add(but_35)

        @self.dp.message_handler(commands=['start'])
        async def command_start(message: types.Message):
            await self.bot.send_message(message.from_user.id, 'Привет, выберите команду Task_parser!', reply_markup=keybut_1)

        @self.dp.message_handler(commands=['Task_parser'], state=None)
        async def command_start(message: types.Message):
            await Data_parse.choosing_topic.set()
            await self.bot.send_message(message.from_user.id, 'Я могу перебирать задачи по 10 шт в \
                                        выборке. Какую тему вы хотите выбрать?', reply_markup=keybut_2)

        # @self.dp.callback_query_handler(state=Data_parse.choosing_topic)
        # async def input_topic(call: types.CallbackQuery, state: FSMContext):
        #     async with state.proxy() as data:
        #         data['topic'] = call.data
        @self.dp.message_handler(content_types=['text'], state=Data_parse.choosing_topic)
        async def input_topic(message: types.Message):
            if message.text == '/brute':
                self.param['topic'] = 'brute'
            elif message.text == '/math':
                self.param['topic'] = 'math'
            elif message.text == '/strings':
                self.param['topic'] = 'strings'
            elif message.text == '/greedy':
                self.param['topic'] = 'greedy'
            elif message.text == '/implementation':
                self.param['topic'] = 'implementation'
            elif message.text == '/sortings':
                self.param['topic'] = 'sortings'
            elif message.text == '/constructive':
                self.param['topic'] = 'constructive'
            elif message.text == '/algorithms':
                self.param['topic'] = 'algorithms'
            elif message.text == '/graph':
                self.param['topic'] = 'graph'
            elif message.text == '/matchings':
                self.param['topic'] = 'matchings'
            elif message.text == '/shortest':
                self.param['topic'] = 'shortest'
            elif message.text == '/paths':
                self.param['topic'] = 'paths'
            elif message.text == '/Function':
                self.param['topic'] = 'Function'
            elif message.text == '/Problem':
                self.param['topic'] = 'Problem'
            elif message.text == '/structures':
                self.param['topic'] = 'structures'
            elif message.text == '/hashing':
                self.param['topic'] = 'hashing'
            elif message.text == '/search':
                self.param['topic'] = 'search'
            elif message.text == '/binary':
                self.param['topic'] = 'binary'
            elif message.text == '/number':
                self.param['topic'] = 'number'
            elif message.text == '/theory':
                self.param['topic'] = 'theory'
            elif message.text == '/dp':
                self.param['topic'] = 'dp'
            elif message.text == '/pointers':
                self.param['topic'] = 'pointers'
            elif message.text == '/parsing':
                self.param['topic'] = 'parsing'
            elif message.text == '/expression':
                self.param['topic'] = 'expression'
            elif message.text == '/two':
                self.param['topic'] = 'two'
            elif message.text == '/*special':
                self.param['topic'] = '*special'
            elif message.text == '/data':
                self.param['topic'] = 'data'
            elif message.text == '/bitmasks':
                self.param['topic'] = 'bitmasks'

            # await call.message.answer('Выберите сложность задач', reply_markup=keybut_3)
            await Data_parse.next()
            await message.reply('Выберите сложность задач', reply_markup=keybut_3)

        @self.dp.message_handler(state=Data_parse.choosing_difficulty)
        async def input_difficulty(message: types.Message):
            if message.text == '/800':
                self.param['difficulty'] = 800
            elif message.text == '/900':
                self.param['difficulty'] = 900
            elif message.text == '/1000':
                self.param['difficulty'] = 1000
            elif message.text == '/1100':
                self.param['difficulty'] = 1100
            elif message.text == '/1200':
                self.param['difficulty'] = 1200
            else:
                self.param['difficulty'] = 1300

            self.parse()
            await Data_parse.next()


            for index, task in enumerate(self.list_tasks):
                await self.bot.send_message(message.from_user.id, f'{index+1} : name № - {task[0]}, topic - {task[1]}, difficulty - {task[2]}, quantity_solved - {task[3]}')

            await message.reply('Чтоб посмотреть детали задачи наберите имя задачи?', reply_markup=ReplyKeyboardRemove())
            self.list_tasks = [].copy()

        @self.dp.message_handler(state=Data_parse.get_detail)
        async def input_name_n(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                self.param['name_n'] = message.text

            self.detail_task()

            await self.bot.send_message(message.from_user.id, f'name № - {self.task_detail[0]}, topic - {self.task_detail[1]}, difficulty - {self.task_detail[2]}, quantity_solved - {self.task_detail[3]}', reply_markup=keybut_1)

            await Data_parse.next()

        @self.dp.message_handler()
        async def echo_send(message: types.Message):
            await message.answer("Неизвестная команда!")

        executor.start_polling(self.dp, skip_updates=True)


    def parse(self):
        """Функция передачи запроса на 10 задач, полученного от бота в бд и формирование ответа
        """
        if self.param['topic'] != 0 and self.param['difficulty'] != 0:
            topic = self.param['topic']
            difficulty = self.param['difficulty']
            tasks = self.task_base.task_req(topic, difficulty)
            self.list_tasks = tasks.copy()
        self.param = copy.deepcopy(self.new_param)


    def detail_task(self):
        """Функция передачи запроса на детализацию задачи, полученного от бота в бд и формирование ответа
        """
        if self.param['name_n'] != 0:
            name_n = self.param['name_n']
            task_detail = self.task_base.task_detail(name_n)
            self.task_detail = task_detail.copy()
        self.param = copy.deepcopy(self.new_param)
