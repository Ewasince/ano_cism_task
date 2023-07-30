from abc import ABC, abstractmethod
from typing import List

from storage.database_schema import Users


class IUsersStorage(ABC):

    @abstractmethod
    async def create_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    async def read_user(self, user: Users) -> List[Users]:
        pass

    @abstractmethod
    async def update_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    async def delete_user(self, user: Users) -> Users:
        pass
