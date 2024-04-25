from unittest import TestCase
from unittest.mock import ANY, patch, MagicMock
from source.services import task_parser




class TestParser(TestCase):

    @patch('source.services.task_parser')
    def test_task_parser(self, mock_task_parser):
        mock_task_parser = MagicMock()
        mock_task_parser.get.return_value = [
            ['Watermelon № 4A', 'brute', '800', ANY],
            ['Team Olympiad № 490A', 'greedy', '800', ANY]
            ]

        self.assertEqual(task_parser()[0], ['Watermelon № 4A', 'brute', '800', ANY])


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
