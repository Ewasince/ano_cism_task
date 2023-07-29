from abc import ABC, abstractmethod

from storage.database_schema import Users


class IUsersStorage(ABC):

    @abstractmethod
    def create_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    def read_user(self, id_: int) -> Users:
        pass

    @abstractmethod
    def update_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    def delete_user(self, id_: int) -> Users:
        pass
