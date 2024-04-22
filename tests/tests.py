from unittest import TestCase
from unittest.mock import AsyncMock, patch, MagicMock

from source.services import task_parser
from source.classes import Io_telebot, Task_base

import pytest
# from aiogram.filters import Command
# from test_bot import callback_query_handler
# from test_bot import callback_query_handler_with_state
# from test_bot import command_handler
# from test_bot import message_handler
# from test_bot import message_handler_with_state
# from test_bot import message_handler_with_state_data
# from test_bot import States
# from test_bot import TestCallbackData

# from aiogram_tests import MockedBot
# from aiogram_tests.handler import CallbackQueryHandler
# from aiogram_tests.handler import MessageHandler
# from aiogram_tests.types.dataset import CALLBACK_QUERY
# from aiogram_tests.types.dataset import MESSAGE


# class TestParser(TestCase):

#     @patch('source.services.task_parser')
#     def test_task_parser(self, mock_task_parser):
#         mock_task_parser = MagicMock()
#         mock_task_parser.get.return_value = [
#             ['Watermelon № 4A', 'brute', '800', '478582'],
#             ['Team Olympiad № 490A', 'greedy', '800', '55133']
#             ]

#         self.assertEqual(task_parser()[0], ['Watermelon № 4A', 'brute', '800', '478583'])


class TestTaskbase(TestCase):
    @patch('source.classes.Task_base')
    def test_task_base_req(self, MockTaskbase):
        task_base = MockTaskbase()

        task_base.task_req.return_value = [
            ['Odd Divisor № 1475A', 'math', '900', '54711'],
            ['Even Odds № 318A', 'math', '900', '105592']
            ]

        self.assertEqual(task_base.task_req('math', '900'), [
            ['Odd Divisor № 1475A', 'math', '900', '54711'],
            ['Even Odds № 318A', 'math', '900', '105592']
            ])


    @patch('source.classes.Task_base')
    def test_task_base_detail(self, MockTaskbase):
        task_base = MockTaskbase()

        task_base.task_detail.return_value = ['Odd Divisor № 1475A', 'math', '900', '54711']

        self.assertEqual(task_base.task_detail('Odd Divisor № 1475A'), ['Odd Divisor № 1475A', 'math', '900', '54711'])


    # @patch('source.classes.Task_base')
    # def test_task_base_fill_db(self, create_engine_mock):

    #     enginemock = MagicMock()

    #     create_engine_mock.return_value = enginemock.engine
    #     enginemock.create_session(enginemock.engine).add(Task('Odd Divisor № 1475A', 'math', '900', '54711')).commit()



# @pytest.mark.asyncio
# async def test_command_handler():
#     telebot = Io_telebot().bot
#     teledp = Io_telebot().dp
#     telebut = Io_telebot().keybut_1
#     message = AsyncMock()
#     await command_start(message)
#     telebot.send_message.assert_called_with('Привет, выберите команду Task_parser!', reply_markup=telebut)
