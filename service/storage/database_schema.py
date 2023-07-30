import sqlalchemy as sa
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


class Base(DeclarativeBase):

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(Base):
    __tablename__ = "user_account"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    login = sa.Column(sa.String(length=50), unique=True, nullable=False)
    password = sa.Column(sa.String(length=256), nullable=False)

    pass


if __name__ == '__main__':
    test = Users()
    test1: Users = Users(login='aaa')
    test2 = test1.as_dict()
    pass
