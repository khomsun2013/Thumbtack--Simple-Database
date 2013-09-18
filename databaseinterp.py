mport sys

class DatabaseInterpreter:
    def __init__(self,prog):
         self.prog = prog
    def run(self):
        self.vars   = {}            # All variables
        self.error  = 0              # Indicates program error
        self.stat = list(self.prog)  # Ordered list of all line numbers
        self.stat.sort()
        self.pc = 0                  # Current program counter
        self.total = len(self.stat)
        self.trans = []
        self.data = {}
        self.commit = False 
        t = -1
        while self.pc < self.total:
            line  = self.stat[self.pc]
            instr = self.prog[line]
            op = instr[0]            
            if op == 'SET':
                 target = instr[1]
                 value  = instr[2]
                 self.vars[target] = value
            elif op == 'GET':
                 target = instr[1]
                 if self.vars[target]: 
                    print self.vars[target]
                 else: 
                    print "NULL"                
            elif op == 'UNSET':
                 target = instr[1]
                 self.vars[target] = None
            elif op == 'NUMEQUALTO':
                 target = instr[1]
                 count = 0
                 for ele in self.vars:
                     if self.vars.get(ele, target) == target: count = count + 1
                 print count
            elif op == 'BEGIN':
                 if self.vars != {}:
                    t = t + 1
                    self.trans.append(self.vars.copy())
            elif op == 'ROLLBACK':
                 if t != -1:
                    self.vars.update(self.trans[t])
                    self.trans.pop()    
                    t = t - 1
                 else:
                    if self.commit : print "NO TRANSACTION"
                    for ele in self.vars:
                        self.vars[ele] = None                       
            elif op == 'COMMIT':
                 if t != -1:
                    self.data = self.vars.copy() 
                 else:
                    print "NO TRANSACTION"
                 t = -1
                 self.trans = []
                 self.commit = True                    
            self.pc += 1
        
    # Insert statements
    def add_statements(self,prog):
         for line,stat in prog.items():
              self.prog[line] = stat
