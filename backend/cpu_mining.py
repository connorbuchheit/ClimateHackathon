import time
import psutil
from multiprocessing import Pool
from queue import Queue

# Task statuses
STATUS_NOT_STARTED = "NOT_STARTED"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_COMPLETED = "COMPLETED"
STATUS_FAILED = "FAILED"

class JobScheduler:
    def __init__(self, tasks, threshold=50, max_processes=2):
        """
        Initialize the JobScheduler.
        :param tasks: List of task IDs to execute.
        :param threshold: CPU usage limit as a percentage.
        :param max_processes: Number of parallel processes to use.
        """
        self.tasks = tasks
        self.task_status = {task_id: STATUS_NOT_STARTED for task_id in tasks}
        self.threshold = threshold
        self.max_processes = max_processes
        self.queue = Queue()
        for task_id in tasks:
            self.queue.put(task_id)

    def simulate_heavy_task(self, task_id):
        """
        Simulate a CPU-intensive task by performing dummy computations.
        :param task_id: ID of the task.
        :return: Task result as a string.
        """
        try:
            print(f"Task {task_id} started.")
            result = 0
            for i in range(10**7):  # Simulated workload
                result += i % 7
            print(f"Task {task_id} completed.")
            return STATUS_COMPLETED, f"Task {task_id} completed with result {result}"
        except Exception as e:
            print(f"Task {task_id} failed with error: {e}")
            return STATUS_FAILED, f"Task {task_id} failed with error: {e}"

    def monitor_cpu_usage(self):
        """
        Monitor the system's CPU usage.
        :return: True if the CPU is under the threshold, False otherwise.
        """
        usage = psutil.cpu_percent(interval=1)
        print(f"Current CPU usage: {usage}%")
        return usage < self.threshold

    def process_tasks(self):
        """
        Process tasks in the queue while respecting CPU and job limits.
        """
        with Pool(processes=self.max_processes) as pool:
            results = []
            while not self.queue.empty():
                while not self.monitor_cpu_usage():
                    print("CPU usage too high. Waiting...")
                    time.sleep(1)

                task_id = self.queue.get()
                self.task_status[task_id] = STATUS_IN_PROGRESS

                result = pool.apply_async(self.simulate_heavy_task, args=(task_id,))
                results.append((task_id, result))

            # Collect results and update statuses
            for task_id, result in results:
                status, message = result.get()
                self.task_status[task_id] = status
                print(message)

    def retry_failed_tasks(self):
        """
        Retry any tasks that failed during the first run.
        """
        failed_tasks = [task_id for task_id, status in self.task_status.items() if status == STATUS_FAILED]
        print(f"Retrying failed tasks: {failed_tasks}")
        if failed_tasks:
            self.queue = Queue()
            for task_id in failed_tasks:
                self.queue.put(task_id)
            self.process_tasks()

if __name__ == "__main__":
    # Example list of 5 tasks
    task_list = list(range(5))
    scheduler = JobScheduler(task_list, threshold=60, max_processes=2)

    # First round of task processing
    scheduler.process_tasks()

    # Retry any failed tasks
    scheduler.retry_failed_tasks()

    # Print final statuses
    print("Final Task Statuses:")
    for task_id, status in scheduler.task_status.items():
        print(f"Task {task_id}: {status}")
