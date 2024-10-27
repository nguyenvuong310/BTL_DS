from dask import delayed
from dask.distributed import Client


client = Client('192.168.1.39:8786', timeout='60s')
print("Dask client:", client)

@delayed
def calculate_pi(n_terms):
    pi_approx = 0
    for k in range(n_terms):
        pi_approx += ((-1) ** k) / (2 * k + 1)
    return 4 * pi_approx
    
# Divide the work of calculating pi into small parts to increase performance
n_terms = 10**8
n_chunks = 10
chunk_size = n_terms // n_chunks

# Create smaller tasks to calculate each part of the Leibniz series in parallel
tasks = [calculate_pi(chunk_size) for _ in range(n_chunks)]
pi_value = delayed(sum)(tasks) / n_chunks


pi_result = pi_value.compute()
print(f"The approximate value of pi with {n_terms} terms is: {pi_result}")


client.close()