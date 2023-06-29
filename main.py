import heapq


# Task class to represent each task
class Task:
    def __init__(self, name, type, duration):
        self.name = name
        self.type = type
        self.duration = duration
        self.status = "Ready"
        self.execution_time = 0

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        # Compare tasks based on priority
        priorities = {"Z": 1, "Y": 2, "X": 3}
        return priorities[self.type] < priorities[other.type]


# Scheduler class
class Scheduler:
    def __init__(self, resources):
        self.resources = resources  # Available resources
        self.priority_queue = []  # Priority queue of tasks
        self.waiting_queue = []  # Waiting queue of tasks

    def add_task(self, task):
        heapq.heappush(self.priority_queue, (task.type, task))

    def allocate_resources(self, task):
        required_resources = self.get_required_resources(task)
        for resource, count in required_resources.items():
            if self.resources[resource] < count:
                return False
        for resource, count in required_resources.items():
            self.resources[resource] -= count
        task.status = "Running"
        return True

    def release_resources(self, task):
        required_resources = self.get_required_resources(task)
        for resource, count in required_resources.items():
            self.resources[resource] += count

    def get_required_resources(self, task):
        required_resources = {
            "R1": 0,
            "R2": 0,
            "R3": 0,
        }
        if task.type == "X":
            required_resources["R1"] = 1
            required_resources["R2"] = 1
        elif task.type == "Y":
            required_resources["R2"] = 1
            required_resources["R3"] = 1
        elif task.type == "Z":
            required_resources["R1"] = 1
            required_resources["R3"] = 1
        return required_resources

    def execute_task(self, task):
        task.execution_time += 1
        if task.execution_time == task.duration:
            task.status = "Finished"
            self.release_resources(task)
        else:
            task.status = "Ready"

    def run(self):
        time = 0

        while self.priority_queue or self.waiting_queue:
            print("Time:", time)
            print("Resources:", self.resources)
            print("Priority Queue:", [task for _, task in self.priority_queue])
            print("Waiting Queue:", self.waiting_queue)

            if self.priority_queue:
                _, current_task = heapq.heappop(self.priority_queue)
                if not self.allocate_resources(current_task):
                    self.waiting_queue.append(current_task)
                    continue

            for _, task in self.priority_queue:
                if task is not current_task:
                    task.status = "Waiting"

            self.execute_task(current_task)

            for waiting_task in self.waiting_queue:
                if self.allocate_resources(waiting_task):
                    self.waiting_queue.remove(waiting_task)
                    heapq.heappush(
                        self.priority_queue, (waiting_task.type, waiting_task)
                    )

            time += 1
            print("Processor State:", current_task)


# Example usage
if __name__ == "__main__":
    resources = {
        "R1": 1,
        "R2": 2,
        "R3": 1,
    }

    scheduler = Scheduler(resources)

    # User Input:
    num_resources = int(input("Enter the number of resources for R1, R2, R3: "))
    for i in range(num_resources):
        resource_count = int(input(f"Enter the count for resource R{i+1}: "))
        resource_name = f"R{i+1}"
        resources[resource_name] = resource_count

    num_tasks = int(input("Enter the number of tasks: "))
    for i in range(num_tasks):
        task_input = input(
            "Enter task details (Task_Name Task_Type Task_Duration): "
        ).split()
        task_name, task_type, task_duration = task_input
        task = Task(task_name, task_type, int(task_duration))
        scheduler.add_task(task)

    scheduler.run()
