import time


_TRANSIENT_ERRORS = (TimeoutError, ConnectionError, OSError)


def retry(fn, attempts=3, base_delay=0.1, sleep=time.sleep):
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for retry_index in range(attempts):
        try:
            return fn()
        except _TRANSIENT_ERRORS:
            if retry_index == attempts - 1:
                raise
            sleep(base_delay * (2 ** retry_index))
