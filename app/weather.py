import asyncio
import aiohttp

from typing import Any


class WeatherTaskRunner:  # todo rename
    def __init__(self):
        self.tasks = []
        self.current_tasks = []

    async def execute_tasks(self):
        result = []
        while self.tasks:
            current_tasks = self.get_task_to_execute()
            result += await self.gather_tasks(current_tasks)
        return result

    async def gather_tasks(self, current_tasks):
        print('debug info')
        async with aiohttp.ClientSession() as session:
            asyncio_tasks = [asyncio.create_task(self.collect_data_from_api(task, session)) for task in current_tasks]
            results = await asyncio.gather(*asyncio_tasks)
        return results

    async def collect_data_from_api(self, task: dict, session: aiohttp.ClientSession):
        try:
            response = await session.get(task['url'])
            if response.ok:
                data = await response.json()
                return self.postprocess_data(data)
            else:
                raise Exception('Some exception')
        except Exception as e:
            # TODO do a err handling + retry mechanism
            raise e

    def create_task(self):
        task = 'placeholder'  # todo change
        self.tasks.append(task)

    def get_task_to_execute(self, max_tasks=1):
        """
        This is the buffer, to handle failed tasks.
        :param max_tasks:
        :return:
        """
        self.current_tasks, self.tasks = self.tasks[:max_tasks], self.tasks[max_tasks:]
        return self.current_tasks

    def postprocess_data(self, data: dict[str, Any]):
        keys_to_keep = ['name', 'main', 'wind', 'clouds']
        cleaned_data = {k: data.get(k) for k in keys_to_keep}
        return cleaned_data
