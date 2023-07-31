import asyncio
import json
from unittest import IsolatedAsyncioTestCase

from api.dto.user_creds import UserCreds

from api.user_api import salt_the_pass
from storage.users_storage_repository import UsersStorageRepository
import service.api.user_api as users_api


class TestUsersApi(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            pass
        # loop.close()

        self.user_storage: UsersStorageRepository = UsersStorageRepository()

        self.user_creds = UserCreds(login='test_user', password='test_password')
        self.user_creds2 = UserCreds(login='test_user2', password='test_password2')
        self.user_creds3 = UserCreds(login='test_user3', password='test_password2')

        self.user_wrong_creds1 = UserCreds(login='test_user', password='test_password1')
        self.user_wrong_creds2 = UserCreds(login='test_user2', password='test_password')

        await self.user_storage.clear_users()

        pass

    async def test_registration_not_exist(self):
        await users_api.registration(self.user_creds)

        res = await users_api.authentication(self.user_creds)

        expected = True
        print(f'{expected=}')
        actual = res
        print(f'{actual=}')

        self.assertEqual(expected, actual)
        pass

    async def test_registration_exist(self):
        await users_api.registration(self.user_creds)

        with self.assertRaises(Exception):
            # try:
            #     await users_api.registration(self.user_creds)
            # except Exception as e:
            #     raise e
            # finally:
            #     users_api.user_storage._engine.dispose()
            await users_api.registration(self.user_creds)
            pass
        pass

    async def test_authentication_not_exist(self):
        res = await users_api.authentication(self.user_creds)

        expected = False
        print(f'{expected=}')
        actual = res
        print(f'{actual=}')

        self.assertEqual(expected, actual)
        pass

    async def test_authentication_exist_true_creds(self):
        await users_api.registration(self.user_creds)

        res = await users_api.authentication(self.user_creds)

        expected = True
        print(f'{expected=}')
        actual = res
        print(f'{actual=}')

        self.assertEqual(expected, actual)
        pass

    async def test_authentication_exist_wrong_creds_1(self):
        await users_api.registration(self.user_creds)

        res = await users_api.authentication(self.user_wrong_creds1)

        expected = False
        print(f'{expected=}')
        actual = res
        print(f'{actual=}')

        self.assertEqual(expected, actual)
        pass

    async def test_authentication_exist_wrong_creds_2(self):
        await users_api.registration(self.user_creds)

        res = await users_api.authentication(self.user_wrong_creds2)

        expected = False
        print(f'{expected=}')
        actual = res
        print(f'{actual=}')

        self.assertEqual(expected, actual)
        pass

    async def test_list_users(self):
        await users_api.registration(self.user_creds)
        await users_api.registration(self.user_creds2)
        await users_api.registration(self.user_creds3)

        res: dict | list = await users_api.list_users()

        expected = [self.user_creds.login, self.user_creds2.login, self.user_creds3.login]
        print(f'{expected=}')
        actual = res
        print(f'{actual=}')

        self.assertEqual(expected, actual)

        pass

    async def test_salt_the_pass(self):
        pass1 = 'qwerty123'
        pass2 = 'qwerty1234'

        case1 = salt_the_pass(pass1)
        print(f'{case1}')
        case2 = salt_the_pass(pass1)
        print(f'{case2}')

        expected1 = True
        print(f'{expected1=}')
        actual1 = case1 == case2
        print(f'{actual1=}')

        self.assertEqual(expected1, actual1)

        case3 = salt_the_pass(pass1)
        print(f'{case3}')
        case4 = salt_the_pass(pass2)
        print(f'{case4}')

        expected2 = False
        print(f'{expected2=}')
        actual2 = case3 == case4
        print(f'{actual2=}')

        self.assertEqual(expected2, actual2)
        pass
