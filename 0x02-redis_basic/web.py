#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    if url is None or len(url.strip()) == 0:
        return ''
    # Initialize Redis client
    redis_store = redis.Redis()
    # Define keys for caching and request count
    res_key = 'result:{}'.format(url)
    req_key = 'count:{}'.format(url)
    # Try to get the cached result
    result = redis_store.get(res_key)
    # Increment the request count whether cache hit or miss
    redis_store.incr(req_key)
    if result is not None:
        # Decode the result from bytes to string if it's cached
        return result.decode('utf-8')
    # Fetch the result from the URL if not cached
    result = requests.get(url).content.decode('utf-8')
    # Cache the result with an expiration of 10 seconds
    redis_store.setex(res_key, timedelta(seconds=10), result)
    
    return result
