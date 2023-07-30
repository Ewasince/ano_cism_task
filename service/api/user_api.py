import asyncio
import logging as log
import traceback
from hashlib import sha256

from api.dto.user_creds import UserCreds
from storage.database_schema import Users
from storage.i_users_storage import IUsersStorage
from storage.users_storage_repository import UsersStorageRepository

user_storage: IUsersStorage = UsersStorageRepository()


async def registration(user_creds: UserCreds) -> None:
    try:
        salt_password = salt_the_pass(user_creds.password)

        user = Users(login=user_creds.login, password=salt_password)

        user = await user_storage.create_user(user)

        log.info(f'user {user.as_dict()} registered')
    except Exception as e:
        log.warning(f'user {user_creds.login} fail to register, {e=}')
        raise e
        pass
    pass


async def authentication(user_creds: UserCreds) -> bool:
    try:
        salt_password = salt_the_pass(user_creds.password)

        user = Users(login=user_creds.login)
        read_user_list = await user_storage.read_user(user)
        if len(read_user_list) == 0:
            log.info(f'Not authenticated user {user_creds.login}')
            return False

        read_user = read_user_list.pop()

        if read_user.password == salt_password:
            log.info(f'Successfully authenticated user {user_creds.login}')
            return True
        else:
            log.info(f'Not authenticated user {user_creds.login}')
            return False

        pass
    except Exception as e:
        log.warning(f'Authenticate fail user {user_creds.login}, {e=}')
        raise e
        pass
    pass


async def list_users() -> list[str]:
    try:
        user_list = await user_storage.read_user(Users())
        user_logins_list = [u.login for u in user_list]

        log.info(f'Successfully got users list {user_logins_list}')
        return user_logins_list
    except Exception as e:
        log.warning(f'Fail get users list, {e=}')
        traceback.print_exc()
        # print(e.with_traceback())
        raise e
        pass
    pass


def salt_the_pass(password: str) -> str:
    # TODO: засолить пароли
    h = sha256()
    h.update(bytes(password, 'utf-8'))
    return h.hexdigest()
    pass


if __name__ == '__main__':
    async def wrapped():
        test = await list_users()

        # user_creds = UserCreds(login='testlogin2', password='testpasswprd1')
        # user_creds2 = UserCreds(login='testlogin3', password='testpasswprd2')
        # user_creds3 = UserCreds(login='testlogin4', password='testpasswprd3')
        #
        # test2 = await registration(user_creds)
        # test3 = await registration(user_creds2)
        # test4 = await registration(user_creds3)
        pass


    asyncio.run(wrapped())
