import time
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class StatusEnum(Enum):
    OPENED = 'o'
    IN_PROGRESS = 'i'
    CLOSED = 'c'
    pass


class Task(BaseModel):
    task_number: int
    pass


class TaskStatus(BaseModel):
    task_number: int
    status: StatusEnum = StatusEnum.OPENED
    elapsed_time: float
    pass
