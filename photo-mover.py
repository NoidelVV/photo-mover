# pls usa linux
## pls ho usato macOS
# pls usa python3
## fatto
# piazzami in ORIGINALS/ insieme a ordini_15x22.csv e ordini_20x30.csv
## ah... ora ti piazzo
# sputo un sacco di debug, non ti preoccupare
## eh ho notato... più che altro solo debug e quagli poco...

import sys
import os
import shutil

filename_ordini = {'small':'ordini_15x22.csv', 'big':'ordini_20x30.csv'}

def parse_file(filename):
    """ {classe: {vvcodice}]a """
    with open(filename, 'r') as f:
        ordini = {}
        current_classe = ''
        for line in f: 
            line = line[:-1] # trims LF
            l = len(line)
            print(line)
            assert l >= 2
            assert l < 25
            if l == 2:
                current_classe = line.lower()
                print('Found class ' + current_classe)
                ordini[current_classe] = set()
            else:
                # print("Adding %s to %s" % (line, current_classe))
                ordini[current_classe].add(line)
        print('Parsing DONE')
        return ordini

def map_directory(dirname):
    """ Maps vv codici to /path/filename """
    dirmap = {}
    for (path, dirs, files) in os.walk(dirname):
        files = [f for f in files if not f == '.' and not f == "Thumbs.db" and not f == ".DS_Store"] # Skip hidden files and Thumbs.db
        dirs[:] = [d for d in dirs if not d == '.'] # Skip hidden dirs
        if path != '.' and files:
            print("Found class %s" % path)
            for f in files:
                t = os.path.splitext(f)
                # print(t)
                assert t[1] == '.jpg'
                vvcode = t[0].lower()
                dirmap[vvcode] = path + '/' + f

    print("Directory mapping of %s DONE" % dirname)
    return dirmap


if __name__ == '__main__':
    print("Parsing orders' files\n\n")
    ordini = parse_file(filename_ordini['small']) # Change this
    print("\n\nMapping Directory")
    dirmap = map_directory('.')
    errors = []
    for classe in ordini:
        for codice in ordini[classe]:
            print("Copying %s" % codice)
            if not codice.lower() in dirmap:
                print("-- Found error in %s" % codice.lower())
                errors.append(codice.lower())
            else:
                path = dirmap[codice.lower()]
                if not os.path.exists('../PRINTING/' + classe.upper() + '/'):
                    os.makedirs('../PRINTING/' + classe.upper() + '/')
                shutil.copy2(path, ('../PRINTING/' + classe.upper() + '/'))
    print("\n\nErrors list:")
    print(errors)
