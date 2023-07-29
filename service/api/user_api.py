from api.dto.user_creds import UserCreds


async def registration(user_creds: UserCreds) -> None:
    print(f'{user_creds=} registered')
    pass


async def authentication(user_creds: UserCreds) -> bool:
    print(f'{user_creds=} authenticated')

    test_creds = UserCreds(login='adminlogin', password='qwerty123')
    return user_creds == test_creds
    pass


async def list_users() -> list[str]:
    return ['test_user']
    pass
