def apply_batch(state, ops):
    """Apply a batch of add/sub operations and return the resulting dict.

    Atomic: the input ``state`` is never mutated. All operations are
    applied to an internal copy, so if any operation is invalid an
    appropriate ValueError/KeyError is raised and the input is left
    untouched.

    Valid operations are ``(op, key, amount)`` triples where ``op`` is
    ``'add'`` or ``'sub'`` and ``amount`` is a strictly positive plain
    integer. ``sub`` requires the key to exist and may not make the
    balance negative.
    """
    result = dict(state)
    for entry in ops:
        try:
            op, key, amount = entry
        except (TypeError, ValueError):
            raise ValueError(f"invalid operation entry: {entry!r}") from None

        if op not in ("add", "sub"):
            raise ValueError(f"unknown operation: {op!r}")
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ValueError(f"amount must be a strictly positive integer: {amount!r}")

        if op == "add":
            result[key] = result.get(key, 0) + amount
        else:
            if key not in result:
                raise KeyError(key)
            new_balance = result[key] - amount
            if new_balance < 0:
                raise ValueError(f"sub would make balance of {key!r} negative")
            result[key] = new_balance
    return result
