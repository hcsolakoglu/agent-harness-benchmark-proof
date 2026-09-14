"""Atomic batch updates for in-memory ledger state.

The public entry point is :func:`apply_batch`, which applies a batch of
``(op, key, amount)`` operations to a ledger mapping and returns the resulting
state as a brand new mapping.  The caller's mapping is never touched, so the
operation is atomic from the caller's point of view: either every operation is
applied and a new state is returned, or an invalid operation raises and the
original state is left exactly as it was.
"""

__all__ = ["apply_batch"]


def _parse_operation(operation):
    """Return ``(op, key, amount)`` for one entry of ``ops``.

    Raises ``ValueError`` if ``operation`` is not a well formed triple.
    """
    if isinstance(operation, (str, bytes, bytearray)):
        raise ValueError(
            "malformed operation: expected an (op, key, amount) triple, "
            "got {!r}".format(operation)
        )
    try:
        op, key, amount = operation
    except (TypeError, ValueError):
        raise ValueError(
            "malformed operation: expected an (op, key, amount) triple, "
            "got {!r}".format(operation)
        ) from None
    return op, key, amount


def _check_key(key):
    """Reject keys that cannot be used as mapping keys."""
    try:
        hash(key)
    except TypeError:
        raise ValueError(
            "invalid operation: unhashable key {!r}".format(key)
        ) from None


def _check_amount(amount, op, key):
    """Reject anything that is not a strictly positive plain integer."""
    # ``bool`` is a subclass of ``int`` but is not a plain integer, and floats,
    # strings, Decimals, etc. are not amounts the ledger supports either.
    if type(amount) is not int:
        raise ValueError(
            "invalid amount for {!r} on key {!r}: expected a plain integer, "
            "got {}: {!r}".format(op, key, type(amount).__name__, amount)
        )
    if amount <= 0:
        raise ValueError(
            "invalid amount for {!r} on key {!r}: expected a strictly "
            "positive integer, got {!r}".format(op, key, amount)
        )


def apply_batch(state, ops):
    """Apply ``ops`` to ``state`` atomically and return the new state.

    ``state`` is a mapping of ``key -> balance`` and ``ops`` is an iterable of
    ``(op, key, amount)`` triples where:

    * ``op`` is ``'add'`` or ``'sub'``;
    * ``amount`` is a strictly positive plain integer;
    * an ``'add'`` on an unknown key starts from a balance of ``0``;
    * a ``'sub'`` may not make a balance negative and requires the key to
      already exist.

    The input mapping is never mutated: the operations are applied to a copy
    that is returned on success.  Any invalid operation raises ``ValueError``
    (unknown op, bad amount, negative result, malformed entry) or ``KeyError``
    (``'sub'`` on a missing key), leaving the input untouched.
    """
    try:
        new_state = dict(state)
    except TypeError:
        raise TypeError(
            "state must be a mapping of balances, got {}".format(
                type(state).__name__
            )
        ) from None

    for operation in ops:
        op, key, amount = _parse_operation(operation)
        _check_key(key)

        if op == "add":
            _check_amount(amount, op, key)
            new_state[key] = new_state.get(key, 0) + amount
        elif op == "sub":
            _check_amount(amount, op, key)
            if key not in new_state:
                raise KeyError(key)
            balance = new_state[key]
            remaining = balance - amount
            if remaining < 0:
                raise ValueError(
                    "invalid operation: sub of {!r} from key {!r} would make "
                    "the balance negative ({!r})".format(amount, key, balance)
                )
            new_state[key] = remaining
        else:
            raise ValueError(
                "unknown operation {!r}: expected 'add' or 'sub'".format(op)
            )

    return new_state
