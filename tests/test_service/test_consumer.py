from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from freezegun import freeze_time

from message_broker.consumer import callback
from message_broker.dto.task import Task, StatusTask, StatusEnum


class TestConsumer(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.timestamp = 1690800000

    async def test_callback(self):
        # prepare
        channel_mock = Mock()

        task_number = 42
        task = Task(task_number=task_number)

        task_statuses = [
            StatusTask(task_number=task_number, status=StatusEnum.OPENED.value, elapsed_time=0),
            StatusTask(task_number=task_number, status=StatusEnum.IN_PROGRESS.value, elapsed_time=0),
            StatusTask(task_number=task_number, status=StatusEnum.CLOSED.value, elapsed_time=0),
        ]

        # call
        with freeze_time(datetime.fromtimestamp(self.timestamp)):
            callback(channel_mock, None, None, bytes(task.model_dump_json(), 'utf-8'))

            # assert
            channel_mock.basic_publish.assert_called()
            print(channel_mock.basic_publish.call_args_list)

            expected = 3
            print(f'{expected=}')
            call_list = channel_mock.basic_publish.call_args_list
            actual = len(call_list)
            print(f'{actual=}')
            self.assertEqual(expected, actual)

            task_status_expected: StatusTask
            for call_args, task_status_expected in zip(call_list, task_statuses):
                body = call_args.kwargs['body']

                expected = task_status_expected.model_dump_json()
                print(f'{expected=}')
                task_status_actual = StatusTask.model_validate_json(body)
                actual = task_status_actual.model_dump_json()
                print(f'{actual=}')

                self.assertEqual(expected, actual)

            pass

    pass
