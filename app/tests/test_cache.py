import unittest
from unittest.mock import MagicMock, patch
from internal import get_cache, set_cache

class TestCache(unittest.TestCase):
    @patch('internal.cache.redis_client')
    def test_get_cache_hit(self, mock_redis):
        mock_redis.get.return_value = '{"result": "success"}'
        result = get_cache("test_key")
        self.assertEqual(result, {"result": "success"})
        mock_redis.get.assert_called_with("test_key")

    @patch('internal.cache.redis_client')
    def test_get_cache_miss(self, mock_redis):
        mock_redis.get.return_value = None
        result = get_cache("test_key")
        self.assertIsNone(result)

    @patch('internal.cache.redis_client')
    def test_set_cache(self, mock_redis):
        set_cache("test_key", {"data": 123}, ttl=60)
        mock_redis.setex.assert_called_with("test_key", 60, '{"data": 123}')

if __name__ == '__main__':
    unittest.main()
