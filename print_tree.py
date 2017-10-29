import os

def print_tree(dir, print_files=False, indent=4, max_level=None):
    tree = ""
    padding = '|' + ' '*(indent-1)
    for path, dir, files in os.walk(dir):
        level = path.count(os.sep)
        parts = path.split(os.sep)
        if max_level is not None and level > max_level:
            continue
        symbol = ''
        if os.path.isdir(os.path.abspath(path)):
            symbol = os.sep
        if not print_files and symbol != os.sep:
            continue
        tree += padding*level + parts[-1] + symbol + "\n"
    print(tree)
    return tree

print_tree('root', indent=4, max_level=2)