import asyncio
import threading
import multiprocessing
import time

def cpu_task(iterations):
    result = 0
    for i in range(iterations):
        result += i * i
    print(result)

async def i_o_task_async(delay):
    await asyncio.sleep(delay)
    print("I/O bound task complete(async)")

def i_o_task_sync(delay):
    time.sleep(delay)
    print("I/O bound task complete(sync)")

def run_multiprocessing(task_func, num_tasks, *args):
    processes = []
    for _ in range(num_tasks):
        process = multiprocessing.Process(target=task_func, args=args)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

def multithreading(task_func, num_tasks, *args):
    threads = []
    for _ in range(num_tasks):
        thread = threading.Thread(target=task_func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

async def run_asyncio(task_func, num_tasks, *args):
    tasks = [task_func(*args) for _ in range(num_tasks)]
    await asyncio.gather(*tasks)

def performance(name, func, *args):
    start_time = time.perf_counter()
    func(*args)
    end_time = time.perf_counter()
    print(f"{name} lasted for {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    cpu_iterations = 10**5
    i_o_delay = 0.5
    concurrent_tasks = 4

    print("--- CPU-Bound Task Comparison ---")
    performance("Multiprocessing (CPU)", run_multiprocessing, cpu_task, concurrent_tasks, cpu_iterations)
    performance("Multithreading (CPU)", multithreading, cpu_task, concurrent_tasks, cpu_iterations)

    print("\n--- I/O-Bound Task Comparison ---")
    performance("Multithreading (I/O)", multithreading, i_o_task_sync, concurrent_tasks, i_o_delay)

    start = time.perf_counter()
    asyncio.run(run_asyncio(i_o_task_async, concurrent_tasks, i_o_delay))
    end = time.perf_counter()
    print(f"Asyncio (I/O) lasted for {end - start:.2f} seconds.")
