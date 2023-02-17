import time


# this func counts how many times a function is called (made to avoid openAI free account max requests/min error)
def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        print(wrapper.num_calls)
        if wrapper.num_calls == 58:  # actually the limit is 60/min requests
            time.sleep(70)
            wrapper.num_calls = 0
        return func(*args, **kwargs)

    wrapper.num_calls = 0
    return wrapper
