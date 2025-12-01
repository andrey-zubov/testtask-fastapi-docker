import asyncio
import json
import time

import aiohttp
import os

from app.exceptions import InvalidCityException, UnauthorizedException, UnhandledException
from app.utils import postprocess_response


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
        response = await session.get(task['url'])
        task['timestamp'] = int(time.time())
        if response.ok:
            data = await response.json()
            return postprocess_response(data, task)
        else:
            await self.postprocess_error(response, task)


    def create_task(self, city):
        app_id = os.getenv("OpenWeather_APIKey")  # todo move

        task = {
            'city': city,
            'url': f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={app_id}",
        }
        self.tasks.append(task)

    def get_task_to_execute(self, max_tasks=1):
        """
        This is the buffer, to handle failed tasks.
        :param max_tasks:
        :return:
        """
        self.current_tasks, self.tasks = self.tasks[:max_tasks], self.tasks[max_tasks:]
        return self.current_tasks

    async def postprocess_error(self, response: aiohttp.ClientResponse, task: dict):
        try:
            res = await response.json()
            msg = res['message']
        except json.decoder.JSONDecodeError:
            msg = await response.text()

        if response.status in (401, 403):
            raise UnauthorizedException()
        elif response.status == 404:
            raise InvalidCityException(task['city'])
        elif response.status == 500:
            pass  # todo retry
        else:
            raise UnhandledException(msg)
