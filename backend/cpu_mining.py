import time
import psutil
from multiprocessing import Pool

def simulate_heavy_task(task_id):
    """
    Simulate a CPU-intensive task by performing dummy computations.
    :param task_id: ID of the task
    :return: Result of the computation
    """
    result = 0
    for i in range(10**7):  # Simulated workload
        result += i % 7
    return f"Task {task_id} completed with result {result}"

def monitor_cpu_usage(threshold=50):
    """
    Monitor the system's CPU usage.
    :param threshold: CPU usage limit as a percentage
    :return: True if the CPU is under the threshold, False otherwise
    """
    usage = psutil.cpu_percent(interval=1)
    print(f"Current CPU usage: {usage}%")
    return usage < threshold

def mine_cpu(tasks, threshold=50):
    """
    Perform CPU mining tasks while monitoring CPU usage.
    :param tasks: List of tasks to execute
    :param threshold: CPU usage limit as a percentage
    """
    # TODO: Change to dynamic allocation of processors
    with Pool(processes=2) as pool:  
        results = []
        for task in tasks:
            while not monitor_cpu_usage(threshold):
                print(f"CPU usage too high. Waiting...")
                time.sleep(1)  # Wait for 1 second before rechecking
            result = pool.apply_async(simulate_heavy_task, args=(task,))
            results.append(result)

        # Collect results
        for result in results:
            print(result.get())  # Block until the result is ready

if __name__ == "__main__":
    task_list = list(range(5))  # 5 dummy tasks
    mine_cpu(task_list, threshold=60)
