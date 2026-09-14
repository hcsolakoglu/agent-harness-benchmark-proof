import time

# Only these transient errors are retried.  ConnectionError and TimeoutError
# are subclasses of OSError, but they are listed explicitly to document intent
# and remain correct if that hierarchy ever changes.
_TRANSIENT_ERRORS = (TimeoutError, ConnectionError, OSError)


def retry(fn, attempts=3, base_delay=0.1, sleep=time.sleep):
    """Call ``fn`` up to ``attempts`` times, retrying transient errors.

    Only TimeoutError, ConnectionError and OSError are retried.  Between
    attempts the callable sleeps for ``base_delay * 2 ** retry_index`` where
    ``retry_index`` is the zero-based index of the failed attempt.  The final
    transient error is re-raised, non-transient errors propagate immediately,
    and ``attempts < 1`` raises ValueError.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    for i in range(attempts):
        try:
            return fn()
        except _TRANSIENT_ERRORS:
            if i == attempts - 1:
                raise
            sleep(base_delay * (2 ** i))
