import os

def get_size(state, root, names):
    paths = [os.path.realpath(os.path.join(root, n)) for n in names]
    # handles dangling symlinks
    state[0] += sum(os.stat(p).st_size for p in paths if os.path.exists(p))

def print_sizes(root):
    print("calculating...")
    total = 0
    paths = []
    state = [0]
    n_ind = s_ind = 0
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        state[0] = 0
        if not os.path.isdir(path):
            state[0] = os.stat(path).st_size
        else:
            for root2, dirs, files in os.walk(path, topdown=False):
                get_size(state, root2, files + dirs)
        total += state[0]
        s_size = size_string(state[0])
        n_ind = max(n_ind, len(name), 5)
        s_ind = max(s_ind, len(s_size))
        paths.append((name, s_size, state[0]))
    paths.sort(key=customSort)
    for name, size, s in paths:
        print(name.ljust(n_ind), size.rjust(s_ind))
    s_total = size_string(total)
    print('\ntotal'.ljust(n_ind), s_total.rjust(s_ind))

def customSort(k):
    name, s, size = k
    return size

def size_string(size):
    if size > 1099511627776:
        div, mod = divmod(size, 1099511627776)
        str_size = str(div) + "Tb " + size_string(mod)
    elif size > 1073741824:
        div, mod = divmod(size, 1073741824)
        str_size = str(div) + "Gb " + size_string(mod)
    elif size > 1048576:
        div, mod = divmod(size, 1048576)
        str_size = str(div) + "MB " + size_string(mod)
    elif size > 1024:
        div, mod = divmod(size, 1024)
        str_size = str(div) + "Kb " + size_string(mod)
    else:
        str_size = str(size) + "Bytes"
    return str_size

path = input("path: ") or "."
print_sizes(path)