#!/home/tank/Documents/programs/anaconda3/bin/python
#!/home/tank/Documents/programs/anaconda3/bin/python
#!/usr/bin/python
#!/usr/bin/python
#!/usr/bin/python
#!/usr/bin/python
#!/home/tank/Documents/programs/anaconda3/bin/python
#!/home/tank/Documents/programs/anaconda3/bin/python
import sys
import os
import re


HOME=os.environ.get('HOME')
CONFIG_PATH=HOME+'/.config/chmgr.conf'
CONFIG={}
FM={}
REG_P1='^-[husaerblL]$'
REG_P2='^--(help|update|search|add|edit|remove|bookmark|list)$'
REG_NAME='^[a-zA-Z0-9][a-zA-Z0-9\-_]*$'

def options(args):
    if args==[]:
        helps()
    if re.match(REG_P1,args[0]):
        opt=args[0][1]
    elif re.match(REG_P2,args[0]):
        opt=args[0][2]
    elif re.match(REG_NAME,args[0]):
        view(args[0])
        return
    else:
        helps()
    if len(args)<2 and opt not in ['u','l','L']:
        helps()
    elif opt=='h':
        helps()
    elif opt=='u':
        update()
    elif opt=='s':
        search(args[1])
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
    elif opt=='L':
        listall('L')
    else:
        helps()
    
    return

def view(name):
    if not exist(name):
        print('Open failed: file "'+name+'.md" not found.')
        exit()
    os.system(CONFIG['VIEWER']+' '+CONFIG['CHEAT_PATH']+'/'+name+'.md')

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
            cate=''
            tags=[]
            for line in f.readlines():
                if 'Category:'==line[:9]:
                    if line[9:].rstrip().strip()=='':
                        continue
                    flag=0
                    for s in line[9:].rstrip():
                        if s=='`':
                            if flag==0:
                                flag=1
                                continue
                            else:
                                break
                        if flag==1:
                            cate+=s
                if 'Tags:'==line[:5]:            
                    t=''
                    b=False
                    for c in line:
                        if c=='`':
                            b=not b
                        if c!='`' and b is True:
                            t=t+c
                        elif c=='`' and t!='':
                            if t=='untaged':
                                print('Format err: '+name+'.md : "untaged" can not be used for tag.')
                                print('Update failed.')
                                exit()
                            tags.append(t)
                            t=''
                if '---'==line.rstrip().strip():
                    break
            record=name[:-3]+' '+cate
            if cate=='':
                cate='default'
            if tags==[]:
                tags.append('untaged')
            for tag in tags:
                record+=' '+tag
            table.write(record+'\n')
            f.close()
    table.close()
    path=CONFIG['CHEAT_PATH']+'/.bookmarks'
    if not os.path.exists(path):
        os.system('touch '+path)
    bookmarks=open(path,'r')
    bm=[]
    for line in bookmarks.readlines():
        bm.append(line.rstrip())
    bookmarks.close()
    bookmarks=open(path,'w')
    for name in bm:
        if name+'.md' not in lst:
            bm.remove(name)
    for name in bm:
        bookmarks.write(name+'\n')
    bookmarks.close()

def search(expr):
    if bool(CONFIG['AUTO_UPDATE']):
        update()
    table=open(CONFIG['CHEAT_PATH']+'/.table', 'r')
    names=[]
    cates=[]
    tags=[]
    for line in table.readlines():
        name,cate,tag=line.rstrip().strip().split(' ',2)
        if name not in names:
            names.append(name)
        if cate not in cates:
            cates.append(cate)
        for t in tag.split(' '):
            if t not in tags:
                tags.append(t)
    tags.remove('untaged')
    r_n=[]
    r_c=[]
    r_t=[]
    for n in names:
        if re.match(expr,n):
            r_n.append(n)
    for c in cates:
        if re.match(expr,c):
            r_c.append(c)
    for t in tags:
        if re.match(expr,t):
            r_t.append(t)
    print('Results of '+FM['NAME']+FM['BLD']+'Names'+FM['CLR']+':')
    if r_n==[]:
        print('No results',end='')
    for n in r_n:
        print(FM['FNAME']+n+FM['CLR'],end='\t')
    print()
    print('\nResults of '+FM['CATE']+FM['BLD']+'Categories'+FM['CLR']+':')
    if r_c==[]:
        print('No results',end='')
    for c in r_c:
        print(FM['FNAME']+c+FM['CLR'],end='\t')
    print()
    print('\nResults of '+FM['TAGS']+FM['BLD']+'Tags'+FM['CLR']+':')
    if r_t==[]:
        print('No results',end='')
    for t in r_t:
        print(FM['FNAME']+t+FM['CLR'],end='\t')
    print()
    return r_n,r_c,r_t

def add(name):
    if not re.match(REG_NAME,name):
        print('Add failed: file name should start with a letter or a digit, and only consists of letters, digits, "-", "_".')
        exit()
    if exist(name):
        print('Add failed: file "'+name+'.md" already existed.')
        exit()
    title=name
    category='default'
    head='# '+title+'\nCategory: `'+category+'`\n\nTags: \n\n---\n\n'
    f=open(CONFIG['CHEAT_PATH']+'/'+name+'.md','w')
    f.write(head)
    f.close()
    print('Cheatsheet added: '+name)
    if CONFIG['AUTO_UPDATE'].lower() in ['true','t','1']:
        update()   

def edit(name):
    if not exist(name):
        print('Open failed: file "'+name+'.md" not found.')
        exit()
    os.system(CONFIG['EDITOR']+' '+CONFIG['CHEAT_PATH']+'/'+name+'.md')

def remove(names):
    names=list(set(names))
    success=[]
    failed=[]
    for name in names:
        if not exist(name):
            print('Failed: File "'+name+'.md" not found.')
            failed.append(name)
            continue
        os.system('rm '+CONFIG['CHEAT_PATH']+'/'+name+'.md')
        success.append(name)
    print('Removed: ')
    for name in success:
        print(name,end=' ')
    print()
    print('Failed to remove:')
    for name in failed:
        print(name,end=' ')
    print()
    if CONFIG['AUTO_UPDATE'].lower() in ['true','t','1']:
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
    if CONFIG['AUTO_UPDATE'].lower() in ['true','t','1']:
        update()
    if param and (param=='b' or param=='bookmark'):
        bookmarks=open(CONFIG['CHEAT_PATH']+'/.bookmarks','r')
        bm=[]
        for line in bookmarks:
            bm.append(line.rstrip())
        bookmarks.close()
        print('List all bookmarks:')
        if bm==[]:
            print('No bookmarks')
            return
        for n in bm:
            print(n,end='\t')
        print()
        return
    table=open(CONFIG['CHEAT_PATH']+'/.table', 'r')
    datas={}
    sort_t={}
    sort_c={}
    for line in table.readlines():
        name,cate,tags=line.rstrip().strip().split(' ',2)
        datas[name]=[cate,tags.split(' ')]
        for t in tags.split(' '):
            if t not in sort_t:
                sort_t[t]=[]
            sort_t[t].append(name)
        if cate not in sort_c:
            sort_c[cate]=[]
        sort_c[cate].append(name)
    if param:
        if param=='t' or param=='tag':
            print('All cheatsheets sorted by '+FM['BLD']+'TAGS'+FM['CLR']+':')
            if 'untaged' in sort_t:
                untaged=sort_t.pop('untaged')
                sort_t['untaged']=untaged
            for t in sort_t:
                print(FM['TAGS']+FM['BLD']+' '+t+' '+FM['CLR'])
                for n in sort_t[t]:
                    print(FM['FNAME']+n+FM['CLR'],end='\t')
                print('\n')
        if param=='c' or param=='category':
            print('All cheatsheets sorted by '+FM['BLD']+'CATEGORIES'+FM['CLR']+':')
            for c in sort_c:
                print(FM['CATE']+FM['BLD']+' '+c+' '+FM['CLR'])
                for n in sort_c[c]:
                    print(FM['FNAME']+n+FM['CLR'],end='\t')
                print()
        if param=='T' or param=='Tag':
            print('All cheatsheets sorted by '+FM['BLD']+'TAGS'+FM['CLR']+' with details:')
            if 'untaged' in sort_t:
                untaged=sort_t.pop('untaged')
                sort_t['untaged']=untaged
            for t in sort_t:
                print(FM['TAGS']+FM['BLD']+' '+t+' '+FM['CLR'])
                for n in sort_t[t]:
                    print(FM['FNAME']+n+'\t'+FM['FCATE']+datas[n][0],end='\t\t')
                    for t in datas[n][1]:
                        print(FM['FTAGS']+t+FM['CLR'],end=' ')
                    print(FM['CLR'])
                print('\n')
        if param=='C' or param=='Category':
            print('All cheatsheets sorted by '+FM['BLD']+'CATEGORIES'+FM['CLR']+':')
            for c in sort_c:
                print(FM['CATE']+FM['BLD']+' '+c+' '+FM['CLR'])
                for n in sort_c[c]:
                    print(FM['FNAME']+n+'\t'+FM['FCATE']+datas[n][0],end='\t\t')
                    for t in datas[n][1]:
                        print(FM['FTAGS']+t+FM['CLR'],end=' ')
                    print(FM['CLR'])
                print()
        if param=='L':
            print('All cheatsheets:')
            for n in datas:
                print(FM['FNAME']+n+'\t'+FM['FCATE']+datas[n][0],end='\t\t')
                for t in datas[n][1]:
                    print(FM['FTAGS']+t+FM['CLR'],end=' ')
                print(FM['CLR'])
    else:
        print('All cheatsheets:')
        for n in datas:
            print(FM['FNAME']+n+FM['CLR'],end='\t')
        print()

def config():
    CONFIG['CHEAT_PATH']=''
    CONFIG['EDITOR']=''
    CONFIG['VIEWER']=''
    CONFIG['AUTO_UPDATE']='true'
    CONFIG['COLOR_OUTPUT']='true'
    CONFIG['COLOR_BG_NAME']='242'
    CONFIG['COLOR_FG_NAME']='255'
    CONFIG['COLOR_BG_CATE']='130'
    CONFIG['COLOR_FG_CATE']='226'
    CONFIG['COLOR_BG_TAGS']='22'
    CONFIG['COLOR_FG_TAGS']='46'
    FM['CLR']='\033[0m'
    FM['BLD']='\033[1m'
    FM['NAME']=''
    FM['CATE']=''
    FM['TAGS']=''
    FM['FNAME']=''
    FM['FCATE']=''
    FM['FTAGS']=''
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
    flag=0
    for k in CONFIG:
        if CONFIG[k]=='':
            print('Config err: '+k+' not set.')
            flag=1
    if flag==1:
        print()
        print('Please check '+HOME+'/.local/chmgr.conf')
        exit()
    if not os.path.exists(CONFIG['CHEAT_PATH']):
        print('Config err: CHEAT_PATH='+CONFIG['CHEAT_PATH']+' does not exist, check if the path is valid.')
        exit()
    if CONFIG['COLOR_OUTPUT'].lower() in ['true','t','1']:
        FM['NAME']='\033[48;5;'+CONFIG['COLOR_BG_NAME']+';38;5;'+CONFIG['COLOR_FG_NAME']+'m'
        FM['CATE']='\033[48;5;'+CONFIG['COLOR_BG_CATE']+';38;5;'+CONFIG['COLOR_FG_CATE']+'m'
        FM['TAGS']='\033[48;5;'+CONFIG['COLOR_BG_TAGS']+'m\033[38;5;'+CONFIG['COLOR_FG_TAGS']+'m'
        FM['FNAME']='\033[38;5;'+CONFIG['COLOR_FG_NAME']+'m'
        FM['FCATE']='\033[38;5;'+CONFIG['COLOR_FG_CATE']+'m'
        FM['FTAGS']='\033[38;5;'+CONFIG['COLOR_FG_TAGS']+'m'

def helps():
    print('Usage: chmgr Filename \n\tor\n\tchmgr [OPTION] [PARAMS]')
    print('A cheatsheets management tool, for users establishing their own cheatsheet \nlibrary.')
    print()
    print('options:')
    print('  -s, --search EXPR\tSearch cheatsheets by regluar expression')
    print('  -a, --add NAME\tAdd a new cheatsheet with given name')
    print('  -e, --edit NAME\tEdit existed cheatsheet by name')
    print('  -r, --remove NAMES\tRemove one or several cheatsheets by name')
    print('  -b, --bookmark NAMES\tToggle states for cheatsheets whether they are \n\t\t\tbookmarked')
    print('  -l, --list [PARAM]\tList all cheatsheets; use parameter "t" to sort by \n\t\t\ttags, "c" by categories; use "b" to list bookmarks; \n\t\t\tuse "C","T" to show detailed list')
    print('  -L\t\t\tList all cheatsheets with details')
    print('  -u, --update\t\tUpdate cache file, including bookmark list; Set \n\t\t\tAUTO_UPDATE in config to automaticly update after \n\t\t\tadd/edit/remove your cheatsheets')
    print('  -h, --help\t\tShow usage page')
    print()
    exit()

if __name__=='__main__':
    config()
    options(sys.argv[1:])