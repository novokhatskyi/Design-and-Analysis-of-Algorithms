from functools import lru_cache

@lru_cache(maxsize=10)
def fib(n):
    if n <= 1:
        return n
    # print(f"Calculating fib({n})")
    return fib(n-1) + fib(n-2)

if __name__ == "__main__":
  print(fib(10))
  print(fib(30))
  print(fib(9))
  fib.cache_clear()

  print(fib.cache_info())