import unittest

import pytest
from unittest.mock import AsyncMock, patch
from weathercache import WeatherCache


class TestWeatherCache(unittest.TestCase):

    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        cache = WeatherCache()

        with patch.object(cache, "redis", AsyncMock()) as mock_redis:
            mock_redis.get.return_value = '{"temp": 5}'

            await cache.set("minsk", {"temp": 5}, ttl=100)
            mock_redis.set.assert_called()

            data = await cache.get("minsk")
            assert data == {"temp": 5}
