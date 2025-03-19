import random
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.7f} seconds to execute.")
        return result
    return wrapper

@timing_decorator
def dict_gen(n=10_000):
    i = random.randrange(0,10,1)
    return {i: round(random.uniform(0, 10000), 2) for i in range(n)}

@timing_decorator
def list_gen(n):
    return [random.randint(0, 1000) for x in range(n)]

@timing_decorator
def collection_search(coll, n):
    if isinstance(coll, dict):
        if (n in coll.keys()):
            return True
    if isinstance(coll, list):
        if (n in coll):
            return True
    return False


d = dict_gen(100_000)
l = list_gen(100_000)

collection_search(d, 3.89)
collection_search(l, 9)