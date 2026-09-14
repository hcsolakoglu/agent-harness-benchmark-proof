def apply_batch(state, ops):
    for op,key,amount in ops:
        if op=='add': state[key]=state.get(key,0)+amount
        elif op=='sub': state[key]=state.get(key,0)-amount
    return state
