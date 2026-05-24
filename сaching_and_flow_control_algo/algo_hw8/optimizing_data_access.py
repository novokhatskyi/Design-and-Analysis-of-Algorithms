import random
import time
from lru_cache import LRUCache

def range_sum_no_cache(arr, left, right):
    return sum(arr[left:right+1])

def update_no_cache(arr, idx, val):
    arr[idx] = val
    
cache = LRUCache(1000)

def range_sum_with_cache(arr, left, right):
    key = (left, right)
    cached_result = cache.get(key)
    if cached_result != -1:
        return cached_result
    result = sum(arr[left:right+1])
    cache.put(key, result)
    return result

def update_with_cache(arr, idx, val):
    arr[idx] = val
    keys_for_delete = []
    for left, right in cache.cache.keys():
        if left <= idx <= right:
            keys_for_delete.append((left, right))
    for key in keys_for_delete:
        node = cache.cache[key]
        cache.list.remove(node)
        del cache.cache[key]

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        # ~3% запитів — Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% — Range
            if random.random() < p_hot:       # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:                             # 5% — випадкові діапазони
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

if __name__ == "__main__":
    n = 100_000
    q = 50_000

    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    start = time.time()
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            range_sum_no_cache(array, left, right)
        elif query[0] == "Update":
            _, idx, val = query
            update_no_cache(array, idx, val)

    time_no_cache = time.time() - start

    start = time.time()
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            range_sum_with_cache(array, left, right)
        elif query[0] == "Update":
            _, idx, val = query
            update_with_cache(array, idx, val)

    time_with_cache = time.time() - start

    speedup = time_no_cache / time_with_cache

    print(f"Без кешу : {time_no_cache:.2f} c")
    print(f"LRU-кеш  : {time_with_cache:.2f} c  (прискорення ×{speedup:.1f})")
    
"""
Без кешу : 8.99 c
LRU-кеш  : 3.45 c  (прискорення ×2.6)
"""