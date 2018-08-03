#!/home/tank/Documents/programs/anaconda3/bin/python

import sys
import textwrap

CHEAT_PATH=''
CONFIG_PATH=''

def options(args):
    if args==None:
        helps()
    if len(args[0])==2 and args[0][0]=='-':
        opt=args[0][1]
    elif len(args[0])>2 and args[0][:2]=='--' and args[0][2:] in ['help','search','add','edit','remove','bookmark','list']:
        opt=args[0][2]
    else:
        helps()
    if len(args)<2 and opt not in ['l']:
        helps()
    elif opt=='h':
        helps()
    elif opt=='s':
        search(args[1:])
    elif opt=='a':
        add(args[1])
    elif opt=='e':
        edit(args[1])
    elif opt=='r':
        remove(args[1:])
    elif opt=='b':
        bookmark(args[1:])
    elif opt=='l':
        param=None
        if len(args)>1:
            param=args[1]
        listall(param)
    else:
        helps()
    
    return

def search(keywords):
    print(keywords)
    return

def add(name):
    print(name)
    return

def edit(name):
    print(name)
    return

def remove(names):
    print(names)
    return

def bookmark(names):
    print(names)
    return

def listall(param):
    print(param)
    return

def config():
    return

def helps():
    print('Usage: ch [OPTION] [PARAMS]')
    print('A cheatsheets management tool, for users establishing their own cheatsheet \nlibrary.')
    print()
    print('options:')
    print('  -s, --search\t\tSearch files by keywords, support several words in \n\t\t\ta row, keywors can be tags/categories/names, regex \n\t\t\tsupported')
    print('  -a, --add NAME\tAdd a new cheatsheet with given name')
    print('  -e, --edit NAME\tEdit existed cheatsheet by name')
    print('  -r, --remove NAMES\tRemove one or several cheatsheets by name')
    print('  -b, --bookmark NAMES\tToggle states for cheatsheets whether they are \n\t\t\tbookmarked')
    print('  -l, --list [PARAMS]\tList all cheatsheets; use parameter "t" to sort by tags, "c" by \n\t\t\tcategories')
    print('  -h, --help\t\tShow usage page')
    print()
    exit()

if __name__=='__main__':
    config()
    options(sys.argv[1:])