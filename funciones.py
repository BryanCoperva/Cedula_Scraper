def split_name(name):
    name = name.replace('*','').replace('/',' ').rstrip()
    #name.replace('/',' ')
    splited = get_name(name)
    if len(splited) <3:
        nam1 = splited[0]
        nam2 = splited[1]
        return [nam1, nam2, None]
    if len(splited) <4:
        nam1 = splited[0]
        nam2 = splited[1]
        nam3 = splited[2]
        return [nam1, nam2, nam3]
    nam1 = ' '.join(splited[:-2])
    nam2 = splited[-2]
    nam3 = splited[-1]
    return [nam1, nam2, nam3]
def get_name(name, inverse=False):
    flag=0
    skips = ['de', 'los', 'la', 'santa', 'del']
    namedir = name.lower().split(' ')
    new_name = list()
    for i in range(len(namedir)):
        word = namedir[i]
        if flag:
            temp.append(namedir[i-1])
        if word in skips:
            if not flag:
                temp = list()
            flag=1
            continue
        if flag:
            temp.append(namedir[i])
            word = ' '.join(temp)
        new_name.append(word)
        flag = 0
    return new_name