from app.services.cache_service import ticker_cache, CacheService

def test_cache():
    key = "test"
    value = {"price": 100}

    CacheService.set(ticker_cache, key, value)
    result = CacheService.get(ticker_cache, key)

    assert result == value