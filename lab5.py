import sys
import time
import numpy as np
import scipy.sparse

def benchmark_operation(operation, structure, runs=100):
    times = np.array([], dtype=np.float64)
    for _ in range(runs):
        start = time.perf_counter()
        operation(structure)
        end = time.perf_counter()
        times = np.append(times, end - start)

    return np.sum(times) / runs

def count_elements_greater_than_50000(arr):
    if isinstance(arr, np.ndarray):
        return np.sum(arr > 50000)
    elif isinstance(arr, scipy.sparse.spmatrix):
        return arr.data[arr.data > 50000].size

def membership_test(arr):
    return 75000 in arr if isinstance(arr, np.ndarray) else (75000 in arr.data)

def sum(arr):
    if isinstance(arr, np.ndarray):
        return np.sum(arr)
    elif isinstance(arr, scipy.sparse.spmatrix):
        return arr.sum()

def replace(arr):
    if isinstance(arr, np.ndarray):
        arr[arr < 50000] = -1
    elif isinstance(arr, scipy.sparse.spmatrix):
        arr.data[arr.data < 50000] = -1
    return arr

def dot_product(arr):
    if isinstance(arr, np.ndarray):
        return np.dot(arr, arr)
    else:
        return arr.dot(arr)
def generate_values(size):
    return np.random.uniform(50000, 100000, size)

numpy_array = np.random.uniform(0.01, 100000, (1000, 1000))
sparse_matrix = scipy.sparse.random(1000, 1000, density=0.05, data_rvs=generate_values)

operations = {
    "Threshold counting": count_elements_greater_than_50000,
    "Membership test": membership_test,
    "Sum": sum,
    "Replacement": replace,
    "Dot product": dot_product
}

print("Dense Array:")
for name, func in operations.items():
    print(f"{name}: {benchmark_operation(func, numpy_array):.6f} sec")

print("\nSparse Matrix:")
for name, func in operations.items():
    print(f"{name}: {benchmark_operation(func, sparse_matrix):.6f} sec")

print("\nMemory Usage:")
print(f"Dense Array: {numpy_array.nbytes / (1024**2):.5f} MB")
print(f"Sparse Matrix: {(sparse_matrix.data.nbytes + sparse_matrix.row.nbytes + sparse_matrix.col.nbytes) / (1024**2):.5f} MB")