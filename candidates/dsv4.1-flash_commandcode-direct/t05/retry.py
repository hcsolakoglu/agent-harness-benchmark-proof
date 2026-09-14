import time


def retry(fn, attempts=3, base_delay=0.1, sleep=time.sleep):
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for retry_index in range(attempts - 1):
        try:
            return fn()
        except (TimeoutError, ConnectionError, OSError):
            sleep(base_delay * (2 ** retry_index))

    return fn()
