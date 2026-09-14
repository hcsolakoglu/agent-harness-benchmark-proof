"""Retry helper for transient failures.

``retry`` calls ``fn`` up to ``attempts`` times.  Only transient errors
(timeouts, connection failures and other OS-level I/O errors) are retried;
any other exception is propagated to the caller immediately.  When every
attempt fails with a transient error, the last one is re-raised.
"""

import time

#: Errors considered transient and therefore worth retrying.
#: ``ConnectionError`` and ``TimeoutError`` are subclasses of ``OSError``,
#: but they are listed explicitly to document the retry contract.
TRANSIENT_ERRORS = (TimeoutError, ConnectionError, OSError)


def retry(fn, attempts=3, base_delay=0.1, sleep=time.sleep):
    """Call ``fn`` until it succeeds or ``attempts`` transient failures occur.

    Args:
        fn: Zero-argument callable to invoke.
        attempts: Total number of calls to make; must be at least 1.
        base_delay: Delay before the first retry, in seconds.  The delay
            before retry index ``i`` is ``base_delay * 2 ** i``.
        sleep: Callable used to wait between attempts (injectable for tests).

    Returns:
        Whatever ``fn`` returns on its first successful call.

    Raises:
        ValueError: If ``attempts`` is less than 1.
        BaseException: Any non-transient error raised by ``fn`` is
            propagated unchanged.  If all attempts raise a transient error,
            the final transient error is re-raised.
    """
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    last_error = None
    for retry_index in range(attempts):
        try:
            return fn()
        except TRANSIENT_ERRORS as exc:
            last_error = exc
            # Sleep only *between* attempts: no sleep before the first call
            # and no sleep once the final attempt has failed.
            if retry_index + 1 < attempts:
                sleep(base_delay * (2 ** retry_index))

    raise last_error
