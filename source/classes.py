import asyncio
import copy

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

from celery import Celery
from celery.schedules import crontab
app = Celery('classes')
app.config_from_object('celeryconfig')

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage



class Task(Base):
    """

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
    """

    """
    def __init__(self) -> None:
        """

        """
        self.engine = create_engine(DATABASE)
        self.session = self.create_session(self.engine)
        self.create_table('task_parser')


    def create_table(self, table_name):
        """

        """
        if not self.engine.dialect.has_table(self.engine.connect(), table_name):
            Base.metadata.create_all(self.engine)


    @staticmethod
    def create_session(engine):
        """

        """
        Session = sessionmaker(bind=engine)
        return Session()


    @app.task
    async def fill_db(self):
        """

        """
        try:
            all_tasks = await task_parser()

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
            await asyncio.sleep(10)


    async def task_req(self, item):
        """

        """
        print(item)

        session = self.create_session(self.engine)

        tasks_req = session.query(Task).filter(Task.topic == 'math', Task.difficulty == '800',).order_by(Task.id.desc()).limit(10).all()

        all_task_list = []
        for obj in tasks_req:
            task_list = []
            task_list.append(obj.topic)
            task_list.append(int(obj.quantity_solved))
            task_list.append(obj.name_number)
            task_list.append(int(obj.difficulty))
            all_task_list.append(task_list)
        return all_task_list


class Io_telebot:

    new_param = {
            'topic': 0,
            'difficulty': 0
        }

    TOKEN: str = os.getenv('TELEGRAM_TOKEN')

    def __init__(self):
        self.task_base = Task_base
        self.list_tasks = []
        self.param = copy.deepcopy(self.new_param)
        self.bot = Bot(self.TOKEN)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

    def __call__(self):

        class Data_parse(StatesGroup):
            choosing_topic = State()
            choosing_difficulty = State()

        but_1 = KeyboardButton('/Task_parser')
        keybut_1 = ReplyKeyboardMarkup(resize_keyboard=True)
        keybut_1.add(but_1)

        keybut_2 = ReplyKeyboardMarkup(resize_keyboard=True)
        but_2 = KeyboardButton('/brute')
        but_3 = KeyboardButton('/math')
        but_4 = KeyboardButton('/strings')
        keybut_2.add(but_2).add(but_3).add(but_4)

        keybut_3 = ReplyKeyboardMarkup(resize_keyboard=True)
        but_5 = KeyboardButton('/800')
        but_6 = KeyboardButton('/900')
        but_7 = KeyboardButton('/1000')
        but_8 = KeyboardButton('/1100')
        but_9 = KeyboardButton('/1200')
        but_10 = KeyboardButton('/1300')

        keybut_3.add(but_5).add(but_6).add(but_7).add(but_8).add(but_9).add(but_10)

        @self.dp.message_handler(commands=['start', 'help'])
        async def command_start(message: types.Message):
            await self.bot.send_message(message.from_user.id, 'Привет!', reply_markup=keybut_1)

        @self.dp.message_handler(commands=['Task_parser'], state=None)
        async def command_start(message: types.Message):
            await Data_parse.choosing_topic.set()
            await self.bot.send_message(message.from_user.id, 'Я могу перебирать задачи по 10 шт в выборке. Какую тему вы хотите выбрать?', reply_markup=keybut_2)

        @self.dp.message_handler(content_types=['text'], state=Data_parse.choosing_topic)
        async def input_topic(message: types.Message):
            if message.text == '/brute':
                self.param['topic'] = 'brute'
            elif message.text == '/math':
                self.param['topic'] = 'math'
            elif message.text == '/strings':
                self.param['topic'] = 'strings'

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
                await self.bot.send_message(message.from_user.id, f'{index+1} - {task}', reply_markup=keybut_1)

            self.list_tasks = [].copy()
            await Data_parse.next()

        @self.dp.message_handler()
        async def echo_send(message: types.Message):
           await message.answer("Неизвестная команда!")

        executor.start_polling(self.dp, skip_updates=True)


    def parse(self):
        if self.param['topic'] != 0:
            topic = self.param['topic']
            tasks = self.task_base.task_req(topic)
            self.list_tasks = tasks.result().copy()
        self.param = copy.deepcopy(self.new_param)
