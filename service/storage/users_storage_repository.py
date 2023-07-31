import asyncio
from copy import copy
from typing import Self, Optional, List, Never
import logging as log
from sqlalchemy import insert, select, update, delete, Row
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncSession
from sqlalchemy import URL
from sqlalchemy.orm import Mapper, Session

from api.dto.user_creds import UserCreds
from config import config
from storage.database_schema import Users
from storage.i_users_storage import IUsersStorage
from storage.storage_helper import get_url_db


class UsersStorageRepository(IUsersStorage):

    def __init__(self):
        url_object = get_url_db("postgresql+asyncpg")

        self._engine = create_async_engine(url_object)

        self._connection: AsyncConnection = None
        pass

    @staticmethod
    def _async_conn_decorator(func):
        async def wrapped(*args, **kwargs):
            self: Self = args[0]
            try:
                async with self._engine.connect() as conn:
                    self._connection = conn

                    res = await func(*args, **kwargs)

                    await self._connection.commit()

                    return res
                    pass  # -- conn
            except Exception as e:
                raise e
            finally:
                await self._engine.dispose()
                pass  # -- try except finally
            pass  # -- wrapped

        return wrapped

    @_async_conn_decorator
    async def create_user(self, user: Users) -> Users:
        smt = (
            insert(Users).
            values(login=user.login, password=user.password).
            returning(Users)
        )
        res = await self._connection.execute(smt)

        row = res.fetchone()

        user_model = Users(**row._asdict())

        return user_model

    @_async_conn_decorator
    async def read_user(self, user: Users) -> List[Users]:
        smt = (
            select(Users)
        )
        is_passed_user_id = user.id_ is not None
        if is_passed_user_id:
            # noinspection PyTypeChecker
            smt = smt.where(Users.id_ == user.id_)
            pass

        is_passed_user_login = user.login is not None
        if is_passed_user_login:
            # noinspection PyTypeChecker
            smt = smt.where(Users.login == user.login)
            pass

        is_passed_user_password = user.password is not None
        if is_passed_user_password:
            log.warning('read_user not allow find users by password')
            pass

        res = await self._connection.execute(smt)
        rows = res.fetchall()

        is_res_more_than_one = len(rows) > 1
        if (is_passed_user_id
            or is_passed_user_login
            or is_passed_user_password) \
                and is_res_more_than_one:
            raise Exception('More than one users with similar properties')

        user_models = [Users(**row._asdict()) for row in rows]

        return user_models

    @_async_conn_decorator
    async def update_user(self, user: Users) -> Users:
        # noinspection PyTypeChecker
        smt = (
            update(Users).
            where(Users.id_ == user.id_)
        )
        if user.login is not None:
            smt = smt.values(login=user.login)
            pass

        if user.password is not None:
            smt = smt.values(password=user.password)
            pass

        smt = smt.returning(Users)

        res = await self._connection.execute(smt)
        row = res.fetchone()

        user_creds = Users(**row._asdict())

        return user_creds

    @_async_conn_decorator
    async def delete_user(self, user: Users) -> Users:
        # noinspection PyTypeChecker
        smt = (
            delete(Users).
            where(Users.id_ == user.id_).
            returning(Users)
        )

        res = await self._connection.execute(smt)
        row = res.fetchone()

        user_creds = Users(**row._asdict())

        return user_creds

    @_async_conn_decorator
    async def clear_users(self) -> List[Users]:
        # noinspection PyTypeChecker
        smt = (
            delete(Users).
            returning(Users)
        )

        res = await self._connection.execute(smt)
        rows = res.fetchall()

        user_models = [Users(**row._asdict()) for row in rows]

        return user_models

    pass


if __name__ == '__main__':
    async def t():
        user_storage: IUsersStorage = UsersStorageRepository()

        user_add = Users(login='test', password='1234')

        try:
            user_added = await user_storage.create_user(user_add)
            user_added = await user_storage.create_user(user_add)
        except Exception as e:
            pass

        # user_find = Users(login='test')
        #
        # user_found_list = await user_storage.read_user(user_find)
        # user_found = user_found_list.pop()
        #
        # user_update = copy(user_found)
        # user_update.password = 'new password'
        #
        # user_updated = await user_storage.update_user(user_update)
        #
        # user_find2 = Users(login='test')
        # user_found_list2 = await user_storage.read_user(user_find2)
        # user_found2 = user_found_list2.pop()
        #
        # user_delete = user_found2
        # user_deleted = await user_storage.delete_user(user_delete)

        pass


    asyncio.run(t())

    pass
