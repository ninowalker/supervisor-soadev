

def unpack_symbols(sets, graph, *keys):
    procs = []
    seen = set()
    for key in keys:
        if not key or key in seen:
            continue
        if key not in sets:
            seen.add(key)
            procs.append(key)
            continue
        stack = set(graph[key])
        while len(stack):
            key = stack.pop()
            if key in seen:
                continue
            seen.add(key)
            if key not in sets:
                procs.insert(0, key)
            stack.update(graph[key])
    return procs

