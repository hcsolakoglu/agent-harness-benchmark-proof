def _positive_plain_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def apply_batch(state, ops):
    result = dict(state)
    for op, key, amount in ops:
        if op == 'add':
            if not _positive_plain_int(amount):
                raise ValueError(
                    f"add amount for {key!r} must be a strictly positive plain integer, got {amount!r}"
                )
            result[key] = result.get(key, 0) + amount
        elif op == 'sub':
            if not _positive_plain_int(amount):
                raise ValueError(
                    f"sub amount for {key!r} must be a strictly positive plain integer, got {amount!r}"
                )
            if key not in result:
                raise KeyError(key)
            if result[key] - amount < 0:
                raise ValueError(
                    f"sub of {amount!r} from {key!r} would make the balance negative"
                )
            result[key] = result[key] - amount
        else:
            raise ValueError(f"unknown op {op!r}; expected 'add' or 'sub'")
    return result
