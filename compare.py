import time
from dask import delayed
from dask.distributed import Client

# Dask Client for parallel computation
client = Client('192.168.1.39:8786', timeout='60s')
print("Dask client:", client)

# Define the function to calculate pi using the Leibniz series
def calculate_pi_sequential(n_terms):
    pi_approx = 0
    for k in range(n_terms):
        pi_approx += ((-1) ** k) / (2 * k + 1)
    return 4 * pi_approx

@delayed
def calculate_pi_parallel(n_terms):
    pi_approx = 0
    for k in range(n_terms):
        pi_approx += ((-1) ** k) / (2 * k + 1)
    return 4 * pi_approx

# Number of terms and chunks for parallel computation
n_terms = 10**8
n_chunks = 10
chunk_size = n_terms // n_chunks

# Sequential Calculation
start_time = time.time()
pi_seq_result = calculate_pi_sequential(n_terms)
sequential_time = time.time() - start_time
print(f"Sequential Pi calculation with {n_terms} terms: {pi_seq_result}")
print(f"Sequential calculation time: {sequential_time:.2f} seconds")

# Parallel Calculation with Dask
start_time = time.time()
tasks = [calculate_pi_parallel(chunk_size) for _ in range(n_chunks)]
pi_parallel = delayed(sum)(tasks) / n_chunks
pi_parallel_result = pi_parallel.compute()
parallel_time = time.time() - start_time
print(f"Parallel Pi calculation with {n_terms} terms: {pi_parallel_result}")
print(f"Parallel calculation time: {parallel_time:.2f} seconds")

# Close Dask client
client.close()

# Compare results
print("\nComparison:")
print(f"Sequential Result: {pi_seq_result}")
print(f"Parallel Result: {pi_parallel_result}")
print(f"Difference: {abs(pi_seq_result - pi_parallel_result)}")
print(f"Speedup: {sequential_time / parallel_time:.2f}x")