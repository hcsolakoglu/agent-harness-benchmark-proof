def schedule(graph):
    done=set(); out=[]
    while len(done)<len(graph):
        for node,deps in graph.items():
            if node not in done and all(d in done for d in deps):
                done.add(node); out.append(node)
    return out
