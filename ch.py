#!/home/tank/Documents/programs/anaconda3/bin/python

import sys
import os


HOME=os.environ.get('HOME')
CONFIG_PATH=HOME+'/.config/ch.conf'
CONFIG={}


def options(args):
    if args==None:
        helps()
    if len(args[0])==2 and args[0][0]=='-':
        opt=args[0][1]
    elif len(args[0])>2 and args[0][:2]=='--' and args[0][2:] in ['help','update','search','add','edit','remove','bookmark','list']:
        opt=args[0][2]
    else:
        helps()
    if len(args)<2 and opt not in ['u','l']:
        helps()
    elif opt=='h':
        helps()
    elif opt=='u':
        update()
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

def exist(name):
    allfile=os.listdir(CONFIG['CHEAT_PATH'])
    if name+'.md' in allfile:
        return True
    return False

def update():
    table=open(CONFIG['CHEAT_PATH']+'/.table','w')
    lst=os.listdir(CONFIG['CHEAT_PATH'])
    for name in lst:
        if name[-3:]=='.md':
            f=open(CONFIG['CHEAT_PATH']+'/'+name,'r')
            head=[x for x in f.readline().split(' ') if x not in ['#','']][0].rstrip()
            if head[0]=='#':
                head=head[1:]
            cate=[x for x in f.readline().split(':')[1].split(' ') if x not in ['']][0].rstrip()[1:-1]
            f.readline()
            tags=[]
            t=''
            b=False
            for c in f.readline():
                if c=='`':
                    b=not b
                if c!='`' and b is True:
                    t=t+c
                elif c=='`' and t!='':
                    tags.append(t)
                    t=''
            line=head+' '+cate
            for t in tags:
                line+=' '+t
            table.write(line+'\n')
            f.close()
    table.close()
    bookmarks=open(CONFIG['CHEAT_PATH']+'/.bookmarks','r+')
    bm=[]
    for line in f.readlines():
        bm.append(line.rstrip())
    for name in bm:
        if name not in lst:
            bm.remove(name)
    for name in bm:
        bookmarks.write(name+'\n')
    bookmarks.close()

def search(keywords):
    print(keywords)
    return

def add(name):
    if exist(name):
        print('Failed: File "'+name+'.md" already existed.\n')
        exit()
    title=name
    category='default'
    head='# '+title+'\nCategory: `'+category+'`\n\nTags: \n\n---\n\n'
    f=open(CONFIG['CHEAT_PATH']+'/'+name+'.md','w')
    f.write(head)
    f.close()
    if bool(CONFIG['AUTO_UPDATE']):
        update()
        

def edit(name):
    if not exist(name):
        print('Failed: File "'+name+'.md" not found.\n')
        exit()
    os.system(CONFIG['EDITOR']+' '+CONFIG['CHEAT_PATH']+'/'+name+'.md')

def remove(names):
    names=list(set(names))
    for name in names:
        if not exist(name):
            print('Failed: File "'+name+'.md" not found.\n')
            exit()
        os.system('rm '+name+'.md')
    if bool(CONFIG['AUTO_UPDATE']):
        update()

def bookmark(names):
    names=list(set(names))
    path=CONFIG['CHEAT_PATH']+'/.bookmarks'
    if not os.path.exists(path):
        os.system('touch '+path)
    f=open(path,'r')
    bm=[]
    ne=[]
    add=[]
    rm=[]
    for line in f.readlines():
        bm.append(line.rstrip())
    f.close()
    fw=open(path,'w')
    for n in names:
        if not exist(n):
            ne.append(n)
            continue
        if n in bm:
            bm.remove(n)
            rm.append(n)
        else:
            bm.append(n)
            add.append(n)
    for n in bm:
        fw.write(n+'\n')
    fw.close()
    if add:
        lst=''
        print('Add bookmarks:')
        for n in add:
            lst+=n+' '
        print(lst)
    if rm:
        lst=''
        print('Remove bookmarks:')
        for n in rm:
            lst+=n+' '
        print(lst)
    if ne:
        lst=''
        print('File doesn\'t exist:')
        for n in ne:
            lst+=n+' '
        print(lst)

def listall(param):
    print(param)
    return

def config():
    CONFIG['CHEAT_PATH']=''
    CONFIG['EDITOR']='vim'
    CONFIG['AUTO_UPDATE']='true'
    if HOME!=None:
        f=open(CONFIG_PATH,'r')
        i=0
        for line in f.readlines():
            i+=1
            if '#' not in  line and '=' not in line:
                if line.rstrip().strip()!='':
                    print('Config err: line '+str(i)+': Invalid config settings.')
                    exit()
                else:
                    continue
            if line.strip()[0]=='#':
                continue
            elif '#' in line:
                line=line.split('#')[0]
            key, value=line.split('=')
            
            CONFIG[key.rstrip().strip()]=value.rstrip().strip()
        f.close()
    else:
        print("Variable $HOME required but not found.")
        exit()
    for k in CONFIG:
        if CONFIG[k]=='':
            print('Config err: '+k+' not set.')
    if not os.path.exists(CONFIG['CHEAT_PATH']):
        print('Config err: CHEAT_PATH='+CONFIG['CHEAT_PATH']+' does not exist, check if the path is valid.')
        exit()


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
    print('  -l, --list [PARAMS]\tList all cheatsheets; use parameter "t" to sort by \n\t\t\ttags, "c" by categories')
    print('  -u, --update\t\tUpdate cache file, including bookmark list; Set \n\t\t\tAUTO_UPDATE in config to automaticly update after \n\t\t\tadd/edit/remove your cheatsheets')
    print('  -h, --help\t\tShow usage page')
    print()
    exit()

if __name__=='__main__':
    config()
    options(sys.argv[1:])