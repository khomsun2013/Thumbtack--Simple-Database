from ply import *
import databaselex

tokens = databaselex.tokens

def p_program(p):
    '''program : program statement
               | statement'''
    if len(p) == 2 and p[1]:
       p[0] = { }
       line,stat = p[1]
       p[0][line] = stat           
    elif len(p) ==3:
       p[0] = p[1]
       if not p[0]: p[0] = { }
       if p[2]:
           line,stat = p[2]
           p[0][line] = stat

def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1

def p_statement(p):
    '''statement : NUMBER command NEWLINE'''
    if isinstance(p[2],str):
        print("%s %s %s" % (p[2],"AT LINE", p[1]))
        p[0] = None
        p.parser.error = 1
    else:
        lineno = int(p[1])
        p[0] = (lineno,p[2])

def p_statement_interactive(p):
    '''statement : NUMBER END NEWLINE'''
    p[0] = (0, (p[2],0))

def p_statement_blank(p):
    '''statement : NUMBER NEWLINE'''
    p[0] = (0,('BLANK',int(p[1])))

def p_statement_bad(p):
    '''statement : NUMBER error NEWLINE'''
    print("INVALID COMMAND AT LINE %s" % p[1])
    p[0] = None
    p.parser.error = 1

def p_statement_newline(p):
    '''statement : NEWLINE'''
    p[0] = None

def p_command_set(p):
    '''command : SET ID NUMBER'''
    p[0] = ('SET',p[2],p[3])

def p_command_set_bad(p):
    '''command : SET ID error'''
    p[0] = "BAD EXPRESSION IN SET"

def p_command_unset(p):
    '''command : UNSET ID'''
    p[0] = ('UNSET',p[2])

def p_command_unset_bad(p):
    '''command : UNSET error'''
    p[0] = "BAD EXPRESSION IN UNSET"

def p_command_get(p):
    '''command : GET ID'''
    p[0] = ('GET',p[2])

def p_command_get_bad(p):
    '''command : GET error'''
    p[0] = "BAD EXPRESSION IN GET"

def p_command_numequalto(p):
    '''command : NUMEQUALTO NUMBER'''
    p[0] = ('NUMEQUALTO',p[2])

def p_command_numequalto_bad(p):
    '''command : NUMEQUALTO error'''
    p[0] = "BAD EXPRESSION IN NUMEQUALTO"

def p_command_begin(p):
    '''command : BEGIN'''
    p[0] = ('BEGIN',)

def p_command_begin_bad(p):
    '''command : BEGIN error'''
    p[0] = "BAD EXPRESSION IN BEGIN"

def p_command_rollback(p):
    '''command : ROLLBACK'''
    p[0] = ('ROLLBACK',)

def p_command_rollback_bad(p):
    '''command : ROLLBACK error'''
    p[0] = "BAD EXPRESSION IN ROLLBACK"

def p_command_commit(p):
    '''command : COMMIT'''
    p[0] = ('COMMIT',)

def p_command_commit_bad(p):
    '''command : COMMIT error'''
    p[0] = "BAD EXPRESSION IN COMMIT"

def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")

bparser = yacc.yacc()

def parse(data,debug=0):
    bparser.error = 0
    p = bparser.parse(data,debug=debug)
    if bparser.error: return None
    return p
