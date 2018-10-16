from ply import *

keywords = (
    'SET','GET','UNSET','END','NUMEQUALTO','BEGIN','ROLLBACK','COMMIT'
)

tokens = keywords + (
     'ID','NUMBER','NEWLINE'
)

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(debug=0)
