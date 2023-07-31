from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from publisher import get_task_num_func, publish


class TestPublisher(IsolatedAsyncioTestCase):

    def test_count_task_func(self):
        func = get_task_num_func()

        expected1 = 0
        print(f'{expected1=}')
        actual1 = func()
        print(f'{actual1=}')
        self.assertEqual(expected1, actual1)

        expected2 = 1
        print(f'{expected2=}')
        actual2 = func()
        print(f'{actual2=}')
        self.assertEqual(expected2, actual2)

        expected3 = 2
        print(f'{expected3=}')
        actual3 = func()
        print(f'{actual3=}')
        self.assertEqual(expected3, actual3)
        pass

    def test_publish(self):
        channel_mock = Mock()

        publish(channel_mock, b'123', None)

        # assert
        channel_mock.basic_publish.assert_called()
        channel_mock.basic_publish.assert_called_once()
        print(channel_mock.basic_publish.call_args_list)

        expected = 1
        print(f'{expected=}')
        call_list = channel_mock.basic_publish.call_args_list
        actual = len(call_list)
        print(f'{actual=}')
        self.assertEqual(expected, actual)

        call_args = call_list.pop()

        body = call_args.kwargs['body']

        expected = '123'
        print(f'{expected=}')
        actual = str(body, 'utf-8')
        print(f'{actual=}')

        self.assertEqual(expected, actual)

        pass

    pass
