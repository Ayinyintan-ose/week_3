import random
import multiprocessing as mp
import time

def data(large):
    sum_data = sum(large)
    data_count = len(large)
    return sum_data, data_count

def generate_dataset(size=10**6):
    return [random.randint(1, 101) for _ in range(size)]


def transform_chunk(data):
    return [x ** 2 for x in data]

if __name__ == "__main__":
    start_time = time.time()
    dataset = generate_dataset()
    end_time = time.time()
    print(f"The dataset took {end_time - start_time:.2f} seconds to generate.")

    num_of_processes = mp.cpu_count()
    data_size = len(dataset) // num_of_processes
    datas = [dataset[i:i + data_size] for i in range(0, len(dataset), data_size)]

    start_time = time.time()
    with mp.Pool(processes=num_of_processes) as pool:
        results = pool.map(data, datas)

    total_sum = sum(res[0] for res in results)
    total_count = sum(res[1] for res in results)
    mean = total_sum / total_count if total_count > 0 else 0
    end_time = time.time()

    print(f"Parallel processing was completed in {end_time - start_time:.2f} seconds.")
    print(f"Mean of the dataset: {mean:.2f}")

    start_time = time.time()
    with mp.Pool(processes=num_of_processes) as pool:
        transformed_chunks = pool.map(transform_chunk, datas)


    transformed_dataset = [item for data in transformed_chunks for item in data]
    end_time = time.time()

    print(f"Data transformation took {end_time - start_time:.2f} seconds.")
    print(f"First 10 elements of transformed dataset: {transformed_dataset[:10]}")