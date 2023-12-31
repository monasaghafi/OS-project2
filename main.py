from queue import PriorityQueue, Queue


# Class to represent a task
class Task:
    def __init__(self, name, type, duration):
        self.name = name
        self.type = type
        self.duration = duration
        self.status = "Ready"
        self.waiting_time = 0
        self.execution_time = 0
        self.option = 0

    def __lt__(self, other):
        # Comparison for priority queue based on task priority
        priorities = {"Z": 1, "Y": 2, "X": 3}
        if self.option == 1:
            return priorities[self.type] < priorities[other.type]
        elif self.option == 2 and self.waiting_time > 0:
            return ((self.waiting_time + self.duration) / self.duration) > (
                (other.waiting_time + other.duration) / other.duration
            )
        else:
            return self.duration < other.duration


# Function to check if resources are available for a task
def check_resources(task, resources):
    if task.type == "X":
        # allcoting R1 , R2
        return resources[0] >= 1 and resources[1] >= 1
    elif task.type == "Y":
        # allcoting R2 , R3
        return resources[1] >= 1 and resources[2] >= 1
    elif task.type == "Z":
        # allcoting R1 , R3
        return resources[0] >= 1 and resources[2] >= 1
    else:
        return False


def Check_resource_not_available(resources):
    if resources[0] == 0 and resources[1] == 0 and resources[2] == 0:
        return True
    else:
        return False


# Function to allocate resources for a task
def allocate_resources(task, resources):
    if task.type == "X":
        resources[0] -= 1
        resources[1] -= 1
    elif task.type == "Y":
        resources[1] -= 1
        resources[2] -= 1
    elif task.type == "Z":
        resources[0] -= 1
        resources[2] -= 1


# Function to release resources after task completion or interruption
def release_resources(task, resources):
    if task.type == "X":
        resources[0] += 1
        resources[1] += 1
    elif task.type == "Y":
        resources[1] += 1
        resources[2] += 1
    elif task.type == "Z":
        resources[0] += 1
        resources[2] += 1


# Function to update task status and execution time
def update_task_status(task, status):
    # status = {"READY","RUNNING","COMPLETED"}
    task.status = status
    if status == "Running":
        task.execution_time += 1


# Function to print the state of the system
def print_system_state(pq, wq, resources, processor, temp=None):
    print(f"R1: {resources[0]} R2: {resources[1]} R3: {resources[2]}")
    if isinstance(pq, PriorityQueue):
        print(
            "Priority queue:",
            [task.name for task in pq.queue],
        )
    else:
        print(
            "Priority queue:",
            [task.name for task in pq],
        )
    if temp is not None:
        print("temp queue:", [task.name for task in temp])
    print("Waiting queue:", [task.name for task in wq.queue])
    print("Processor state:", end=" ")
    if processor is None:
        print("Idle")
    else:
        print(f"Running task: {processor.name}")


# Function to schedule tasks using Shortest-Job-First (SJF) algorithm
def schedule_sjf(tasks, resources):
    pq = PriorityQueue()
    wq = Queue()

    # Sort tasks based on duration
    sorted_tasks = sorted(tasks, key=lambda x: x.duration)

    # Add tasks to the priority queue
    for task in sorted_tasks:
        pq.put(task)

    processor = None

    while not (pq.empty() and wq.empty() and processor is None):
        print_system_state(pq, wq, resources, processor)

        # Check if processor is idle
        if processor is None:
            # Check if there are any tasks in the priority queue
            if not pq.empty():
                task = pq.get()
                if check_resources(task, resources):
                    allocate_resources(task, resources)
                    update_task_status(task, "Running")
                    processor = task
                else:
                    wq.put(task)
            else:
                # No tasks in the priority queue, check waiting queue
                if not wq.empty():
                    task = wq.get()
                    if check_resources(task, resources):
                        allocate_resources(task, resources)
                        update_task_status(task, "Running")
                        processor = task

        else:
            # If a task is running on the processor
            update_task_status(processor, "Running")
            processor.duration -= 1
            processor.execution_time += 1
            if processor.duration == 0:
                release_resources(processor, resources)
                update_task_status(processor, "Completed")
                processor = None

        # Check waiting queue to see if any tasks can be allocated resources now
        temp_wq = (
            Queue()
        )  # Temporary queue to store tasks that cannot be allocated resources
        while not wq.empty():
            task = wq.get()
            if check_resources(task, resources):
                allocate_resources(task, resources)
                update_task_status(task, "Running")
                processor = task
            else:
                task.waiting_time += 1
                temp_wq.put(task)

        wq = temp_wq


# Function to schedule tasks using First-Come-First-Serve (FCFS) algorithm
def schedule_fcfs(tasks, resources):
    pq = []
    wq = Queue()

    # Add tasks to the priority queue
    for task in tasks:
        pq.append(task)

    processor = None

    while not (len(pq) == 0 and wq.empty() and processor is None):
        print_system_state(pq, wq, resources, processor)

        # Check if processor is idle
        if processor is None:
            # Check if there are any tasks in the priority queue
            if len(pq) > 0:
                task = pq.pop(0)
                if check_resources(task, resources):
                    allocate_resources(task, resources)
                    update_task_status(task, "Running")
                    processor = task
                else:
                    wq.put(task)
            else:
                # No tasks in the priority queue, check waiting queue
                if not wq.empty():
                    task = wq.get()
                    if check_resources(task, resources):
                        allocate_resources(task, resources)
                        update_task_status(task, "Running")
                        processor = task

        else:
            # If a task is running on the processor
            update_task_status(processor, "Running")
            processor.duration -= 1
            processor.execution_time += 1
            if processor.duration == 0:
                release_resources(processor, resources)
                update_task_status(processor, "Completed")
                processor = None

        # Check waiting queue to see if any tasks can be allocated resources now
        temp_wq = (
            Queue()
        )  # Temporary queue to store tasks that cannot be allocated resources
        while not wq.empty():
            task = wq.get()
            if check_resources(task, resources):
                allocate_resources(task, resources)
                update_task_status(task, "Running")
                processor = task
            else:
                task.waiting_time += 1
                temp_wq.put(task)

        wq = temp_wq

    # Function to schedule tasks using Highest-Response-Ratio-Next (HRRN) algorithm


def schedule_hrrn(tasks, resources):
    pq = PriorityQueue()
    wq = Queue()

    # Add tasks to the priority queue
    for task in tasks:
        task.option = 2
        pq.put(task)

    processor = None

    while not (pq.empty() and wq.empty() and processor is None):
        print_system_state(pq, wq, resources, processor)

        # Check if processor is idle
        if processor is None:
            # Check if there are any tasks in the priority queue
            if not pq.empty():
                task = pq.get()
                if check_resources(task, resources):
                    allocate_resources(task, resources)
                    update_task_status(task, "Running")
                    processor = task
                else:
                    wq.put(task)
            else:
                # No tasks in the priority queue, check waiting queue
                if not wq.empty():
                    task = wq.get()
                    if check_resources(task, resources):
                        allocate_resources(task, resources)
                        update_task_status(task, "Running")
                        processor = task

        else:
            # If a task is running on the processor
            update_task_status(processor, "Running")
            processor.duration -= 1
            processor.execution_time += 1
            if processor.duration == 0:
                release_resources(processor, resources)
                update_task_status(processor, "Completed")
                processor = None
        for task in tasks:
            if task != processor:
                task.waiting_time += 1


# Function to schedule tasks using Round Robin (RR) algorithm
def schedule_rr(tasks, resources, time_quantum):
    pq = []
    wq = Queue()
    time = 0
    temp = []
    flag = 0
    # Add tasks to the priority queue
    for task in tasks:
        task.option = 1
        pq.append(task)
    pq.sort()
    processor = None
    while not (len(pq) == 0 and len(temp) == 0 and wq.empty() and processor is None):
        # Check if time quantum is reached for RR
        if processor is not None and time % time_quantum == 0:
            # release_resources(processor, resources)
            update_task_status(processor, "READY")
            temp.append(processor)
            processor = None
        # Check if processor is idle
        while processor is None:
            # Check if there are any tasks in the priority queue
            if len(pq) > 0 and (not Check_resource_not_available(resources)):
                task = pq.pop(0)
                if check_resources(task, resources):
                    allocate_resources(task, resources)
                    update_task_status(task, "Running")
                    processor = task
                else:
                    wq.put(task)
            elif len(temp) > 0:
                task = temp.pop(0)
                update_task_status(task, "Running")
                processor = task
            else:
                # No tasks in the priority queue, check waiting queue
                if not wq.empty():
                    task = wq.get()
                    if check_resources(task, resources):
                        allocate_resources(task, resources)
                        update_task_status(task, "Running")
                        processor = task
                    else:
                        wq.put(task)
                        processor = None
        print(f"t={time}")
        print_system_state(pq, wq, resources, processor, temp)
        # If a task is running on the processor
        update_task_status(processor, "Running")
        processor.duration -= 1
        processor.execution_time += 1
        if processor.duration == 0:
            release_resources(processor, resources)
            update_task_status(processor, "Completed")
            processor = None
            time = 0

        time += 1


# Example usage
if __name__ == "__main__":
    resources_input = input("Enter the number of resources for R1 R2 R3: ").split()
    resources = [int(resource) for resource in resources_input]

    tasks = []
    num_tasks = int(input("Enter the number of tasks: "))
    for _ in range(num_tasks):
        task_input = input(
            "Enter task details (Task_Name Task_Type Task_Duration): "
        ).split()
        task_name, task_type, task_duration = task_input
        task = Task(task_name, task_type, int(task_duration))
        tasks.append(task)

    algorithm_choice = input(
        "Choose the scheduling algorithm:\n1. Shortest-Job-First (SJF)\n2. First-Come-First-Served (FCFS)\n3. Round-Robin (RR)\n4. Highest-Response-Ratio-Next (HRRN)\nChoice: "
    )
    if algorithm_choice == "1":
        schedule_sjf(tasks, resources)
    elif algorithm_choice == "2":
        schedule_fcfs(tasks, resources)
    elif algorithm_choice == "3":
        time_quantum = int(input("Enter the time quantum for Round Robin (RR): "))
        schedule_rr(tasks, resources, time_quantum)
    elif algorithm_choice == "4":
        schedule_hrrn(tasks, resources)
    else:
        print("Invalid choice!")
