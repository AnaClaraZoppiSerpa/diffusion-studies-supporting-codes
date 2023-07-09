import signal
import time

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Timeout occurred")

def timed_experiment(functions, max_iteration_time):
    for func in functions:
        print(f"Starting function {func.__name__}.")
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(max_iteration_time)

        try:
            start_time = time.time()
            func()  # Call the function
            elapsed_time = time.time() - start_time
            print(f"Function {func.__name__} finished after {elapsed_time} seconds.")
        except TimeoutError:
            print(f"Timeout occurred for function {func.__name__}. Moving to the next iteration...")
            continue
        finally:
            signal.alarm(0)

def timed_experiment_with_args(function_calls, max_iteration_time):
    for call in function_calls:
        func = call[0]  # Function to call
        args = call[1:]  # Arguments to pass to the function

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(max_iteration_time)

        try:
            print(f"Starting function {func.__name__} with args {args}.")
            start_time = time.time()
            func(*args)  # Call the function with arguments
            elapsed_time = time.time() - start_time
            print(f"Function {func.__name__} finished after {elapsed_time} seconds.")
        except TimeoutError:
            print(f"Timeout occurred for function {func.__name__}. Moving to the next iteration...")
            continue
        finally:
            signal.alarm(0)
