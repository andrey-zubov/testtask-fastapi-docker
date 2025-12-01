import pytest
import unittest
from unittest.mock import AsyncMock, patch

from weather import WeatherTaskRunner
from weathercache import WeatherCache

class TestWeather(unittest.TestCase):
    @pytest.mark.asyncio
    async def test_create_task(self):
        runner = WeatherTaskRunner(WeatherCache())
        runner.create_task("minsk")

        assert len(runner.tasks) == 1
        assert runner.tasks[0]["city"] == "minsk"


    @pytest.mark.asyncio
    async def test_collect_data_from_api_cached(self):
        cache = WeatherCache()
        runner = WeatherTaskRunner(cache)

        task = {"city": "minsk", "url": "http://fake"}

        with patch.object(cache, "get", AsyncMock(return_value={"cached": 1})):
            res = await runner.collect_data_from_api(task, AsyncMock())
            assert res == {"cached": 1}


    @pytest.mark.asyncio
    async def test_collect_data_from_api_success(self):
        cache = WeatherCache()
        runner = WeatherTaskRunner(cache)

        fake_response = AsyncMock()
        fake_response.ok = True
        fake_response.json.return_value = {"name": "Minsk", "main": {}, "wind": {}, "clouds": {}}

        session = AsyncMock()
        session.get.return_value = fake_response

        with patch.object(cache, "get", AsyncMock(return_value=None)):
            with patch("app.weather.postprocess_response", return_value={"ok": 1}) as post:
                res = await runner.collect_data_from_api({"city": "minsk"}, session)

                assert res == {"ok": 1}
                post.assert_called()
