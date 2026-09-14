import time

TRANSIENT_ERRORS = (TimeoutError, ConnectionError, OSError)


def retry(fn, attempts=3, base_delay=0.1, sleep=time.sleep):
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    for i in range(attempts):
        try:
            return fn()
        except TRANSIENT_ERRORS:
            if i == attempts - 1:
                raise
            sleep(base_delay * (2 ** i))
