import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import databaselex
import databaseparse
import databaseinterp

b = databaseinterp.DatabaseInterpreter({})
i = 0
while 1:
    i = i + 1
    try:
        line = raw_input("[LINE "+str(i)+"] ")
    except EOFError:
        raise SystemExit
    if not line:
       i = i - 1 
       continue
    line = str(i) + " " + line +"\n"
    prog = databaseparse.parse(line)
    if not prog: continue

    keys = list(prog)
    if keys[0] > 0:
         b.add_statements(prog)         
    else:
         stat = prog[keys[0]]
         if stat[0] == 'END':
             try:
                 b.run()
                 break
             except RuntimeError:
                 pass
