import random
import statistics
import time
import numpy as np

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        wrapper.last_execution_time = end_time - start_time
        # print(f"{func.__name__} took {wrapper.last_execution_time:.5f} seconds to execute.")
        return result
    return wrapper

@timing_decorator
def count_elements_greater_than_50000(coll):
    c = 0
    for i in coll:
        for j in i:
            if j > 50000:
                c += 1
    return c

@timing_decorator
def count_equal_to(coll):
    c = 0
    for i in coll:
        for j in i:
            if j == 75000.42:
                c += 1
    return c
@timing_decorator
def sum_and_min(coll):
    s = 0
    min = 100000.0
    for i in coll:
        for j in i:
            s += j
            if j < min:
                min = j
    return s, min

@timing_decorator
def replace(coll):
    for i in coll:
        for j in i:
            if j < 50000:
                j = -1
    return coll


python_list = [[random.uniform(0, 10000) for y in range(1000)] for x in range(1000)]
numpy_list = np.array(python_list)
print(np.allclose(python_list, numpy_list))

python_time = [[] for i in range(4)]
numpy_time = [[] for i in range(4)]

for i in range(10):
    # first task
    t1_p = count_elements_greater_than_50000(python_list)
    python_time[0].append(count_elements_greater_than_50000.last_execution_time)

    start_time = time.perf_counter()
    t1_n = (numpy_list > 50000).sum()
    end_time = time.perf_counter()
    numpy_time[0].append(end_time - start_time)

    # second task
    t2_p = count_equal_to(python_list)
    python_time[1].append(count_equal_to.last_execution_time)

    start_time = time.perf_counter()
    t2_n = (numpy_list == 75000.42).sum()
    end_time = time.perf_counter()
    numpy_time[1].append(end_time - start_time)

    # third task
    t3_p, t3p2 = sum_and_min(python_list)
    python_time[2].append(sum_and_min.last_execution_time)

    start_time = time.perf_counter()
    t3_n, t3n2 = np.min(numpy_list), np.sum(numpy_list)
    end_time = time.perf_counter()
    numpy_time[2].append(end_time - start_time)


    t4_p = replace(python_list)
    python_time[3].append(replace.last_execution_time)

    start_time = time.perf_counter()
    t4_n = numpy_list[numpy_list == 0] = -1
    end_time = time.perf_counter()
    numpy_time[3].append(end_time - start_time)


for i in range(4):
    print(f"Task {i + 1}:")
    print(f"Python: {statistics.median(python_time[i]):.5f}")
    print(f"NumPy: {statistics.median(numpy_time[i]):.5f}")
    print()









