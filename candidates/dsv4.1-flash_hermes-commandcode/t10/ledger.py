"""Atomic batch ledger operations.

``apply_batch`` applies a sequence of credit/debit operations to a mapping of
balances as a single atomic unit.  It never mutates its input: all work happens
on a private copy that is returned only when every operation is valid.
"""


def _is_positive_plain_int(value):
    """True for real integers > 0 (``bool`` is excluded as it is not plain)."""
    return type(value) is int and value > 0


def apply_batch(state, ops):
    """Apply ``ops`` to ``state`` atomically and return the resulting mapping.

    ``ops`` is an iterable of ``(op, key, amount)`` triples where:

    * ``op`` is ``'add'`` (credit) or ``'sub'`` (debit);
    * ``amount`` is a strictly positive plain integer;
    * ``'add'`` creates ``key`` with an implicit balance of ``0`` if absent;
    * ``'sub'`` requires ``key`` to exist and must not drive it negative.

    ``state`` is never modified.  Operations are evaluated in order against the
    running balance of the working copy.  If any operation is invalid the
    matching ``ValueError``/``KeyError`` is raised and the input is left
    untouched.
    """
    working = dict(state)

    for entry in ops:
        try:
            op, key, amount = entry
        except (TypeError, ValueError):
            raise ValueError(
                "each operation must be an (op, key, amount) triple"
            ) from None

        if not _is_positive_plain_int(amount):
            raise ValueError(
                "amount must be a strictly positive plain integer"
            )

        if op == "add":
            working[key] = working.get(key, 0) + amount
        elif op == "sub":
            if key not in working:
                raise KeyError(key)
            balance = working[key] - amount
            if balance < 0:
                raise ValueError(
                    "sub would make the balance for %r negative" % (key,)
                )
            working[key] = balance
        else:
            raise ValueError("unknown operation: %r" % (op,))

    return working
