def longest_unique(text):
    best=''
    for i in range(len(text)):
        for j in range(i+1,len(text)+1):
            s=text[i:j]
            if len(set(s))==len(s) and len(s)>len(best): best=s
    return best
