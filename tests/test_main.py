import asyncio
import unittest
from typing import Tuple

from tasklocal import get_task_local_storage, TaskLocalStorage


class TestCase(unittest.IsolatedAsyncioTestCase):
    name: str

    @classmethod
    def setUpClass(cls):
        cls.name = "tasklocal"

    async def test_multiple_tasks(self) -> None:
        task_1: asyncio.Task
        task_2: asyncio.Task

        (_, task_1), (_, task_2) = await asyncio.gather(
            self._run_task(),
            self._run_task()
        )

        self.assertTrue(task_1.done())
        self.assertTrue(task_2.done())
        self.assertNotEqual(task_1, task_2)

    async def test_weak_ref(self) -> None:
        data, task = await self._run_task()
        self.assertFalse(task.done())
        self.assertEqual(data.name, self.name)

    async def test_weak_ref_done(self) -> None:
        future: asyncio.Future = asyncio.create_task(self._run_task())
        self.assertFalse(future.done())
        data, task = await future
        self.assertTrue(task.done())
        await asyncio.sleep(0)  # Yield control
        with self.assertRaises(ReferenceError):
            print(data.name)

    def test_non_async(self) -> None:
        with self.assertRaises(RuntimeError):
            data = get_task_local_storage()

    async def _run_task(self) -> Tuple[TaskLocalStorage, asyncio.Task]:
        data = get_task_local_storage()
        data.name = self.name
        return data, data.get_task()
