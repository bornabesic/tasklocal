import asyncio
import weakref
from typing import Optional, Dict

__all__ = ["TaskLocalStorage", "get_task_local_storage"]


class TaskLocalStorage:

    def __init__(self, task: asyncio.Task):
        self.__task = task

    def get_task(self) -> asyncio.Task:
        return self.__task

    __setattr__ = object.__setattr__
    __getattribute__ = object.__getattribute__
    __delattr__ = object.__delattr__


def get_task_local_storage(task: Optional[asyncio.Task] = None) -> TaskLocalStorage:
    if task is None:
        task = asyncio.current_task()
        if task is None:
            raise RuntimeError("no running task")

    if task not in _STORAGE:
        task.add_done_callback(lambda t: _STORAGE.pop(t, None))
        _STORAGE[task] = TaskLocalStorage(task)

    storage: TaskLocalStorage = _STORAGE[task]
    return weakref.proxy(storage)


_STORAGE: Dict[asyncio.Task, TaskLocalStorage] = dict()
