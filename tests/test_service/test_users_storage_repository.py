from unittest import TestCase, IsolatedAsyncioTestCase
import logging as log

import sqlalchemy
from sqlalchemy.exc import IntegrityError

# from psycopg2 import IntegrityError

# from sqlalchemy.exc import IntegrityError

from api.user_api import salt_the_pass
from storage.database_schema import Users
from storage.i_users_storage import IUsersStorage
from storage.users_storage_repository import UsersStorageRepository


class TestUsersStorageRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.user_storage: UsersStorageRepository = UsersStorageRepository()
        self.user_for_create = Users(login='test_user', password='test_password')
        self.user_for_create2 = Users(login='test_user2', password='test_password2')
        await self.user_storage.clear_users()

        pass

    async def asyncTearDown(self) -> None:
        await self.user_storage.clear_users()
        pass

    async def test_create_user_one(self):
        # prepare
        user = await self.user_storage.create_user(self.user_for_create)

        user_for_read = Users(id_=user.id_)

        # assert
        read_user_list = await self.user_storage.read_user(user_for_read)
        read_user = read_user_list.pop()

        expected = user.as_dict()
        print(f'{expected=}')
        actual = read_user.as_dict()
        print(f'{actual=}')
        self.assertEqual(expected, actual)
        pass

    async def test_create_user_non_unique(self):
        # prepare
        user = await self.user_storage.create_user(self.user_for_create)

        with self.assertRaises(IntegrityError):
            user2 = await self.user_storage.create_user(self.user_for_create)
            pass
        pass

    async def test_read_user(self):
        # prepare
        user1 = await self.user_storage.create_user(self.user_for_create)

        user_for_read1 = Users(id_=user1.id_)

        user2 = await self.user_storage.create_user(self.user_for_create2)

        user_for_read2 = Users(id_=user2.id_)

        # assert
        read_user1_list = await self.user_storage.read_user(user_for_read1)
        read_user1 = read_user1_list.pop()
        read_user2_list = await self.user_storage.read_user(user_for_read2)
        read_user2 = read_user2_list.pop()

        expected1 = user1.as_dict()
        print(f'{expected1=}')
        actual1 = read_user1.as_dict()
        print(f'{actual1=}')
        self.assertEqual(expected1, actual1)

        expected2 = user2.as_dict()
        print(f'{expected2=}')
        actual2 = read_user2.as_dict()
        print(f'{actual2=}')
        self.assertEqual(expected2, actual2)
        pass

    async def test_update_user(self):
        # prepare
        user = await self.user_storage.create_user(self.user_for_create)
        user_for_update = user
        user_for_update.password = 'new_test_password'
        user_updated = await self.user_storage.update_user(user_for_update)

        user_for_read = Users(id_=user_updated.id_)

        # assert
        read_user_list = await self.user_storage.read_user(user_for_read)
        read_user = read_user_list.pop()

        expected = user_updated.as_dict()
        print(f'{expected=}')
        actual = read_user.as_dict()
        print(f'{actual=}')
        self.assertEqual(expected, actual)
        pass

    async def test_delete_user(self):
        # prepare
        user = await self.user_storage.create_user(self.user_for_create)
        deleted_user = await self.user_storage.delete_user(user)

        user_for_read = Users(id_=user.id_)

        # assert
        read_user_list = await self.user_storage.read_user(user_for_read)

        expected = [i.as_dict() for i in read_user_list]
        print(f'{expected=}')
        actual = []
        print(f'{actual=}')
        self.assertEqual(len(actual), len(expected))
        pass

    async def test_clear_user(self):
        # prepare
        await self.user_storage.create_user(self.user_for_create)
        await self.user_storage.create_user(self.user_for_create2)

        # assert
        clear_user_list = await self.user_storage.clear_users()

        expected = [i.as_dict() for i in clear_user_list]
        print(f'{len(expected)=}')
        actual = 2
        print(f'{actual=}')
        self.assertEqual(actual, len(expected))

        read_user_list = await self.user_storage.read_user(Users())

        expected = [i.as_dict() for i in read_user_list]
        print(f'{expected=}')
        actual = []
        print(f'{actual=}')
        self.assertEqual(len(actual), len(expected))

        pass
