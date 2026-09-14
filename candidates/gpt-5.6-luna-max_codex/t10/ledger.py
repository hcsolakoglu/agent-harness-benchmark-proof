def apply_batch(state, ops):
    """Apply a batch of balance operations without changing ``state``.

    Operations are applied to a private copy so that an invalid operation
    cannot leave the caller's mapping partially updated.
    """
    result = state.copy()

    for operation in ops:
        try:
            op, key, amount = operation
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "each operation must contain an operation, key, and amount"
            ) from exc

        if op not in ("add", "sub"):
            raise ValueError(f"unknown operation: {op!r}")

        if type(amount) is not int or amount <= 0:
            raise ValueError("amount must be a strictly positive integer")

        if op == "add":
            result[key] = result.get(key, 0) + amount
            continue

        if key not in result:
            raise KeyError(key)

        balance = result[key]
        if balance < amount:
            raise ValueError("subtraction would make the balance negative")
        result[key] = balance - amount

    return result
