import time
def retry(fn, attempts=3, base_delay=0.1, sleep=time.sleep):
    for i in range(attempts):
        try:return fn()
        except Exception:
            sleep(base_delay * (2 ** i))
    return None
