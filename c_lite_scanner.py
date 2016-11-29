import ply.lex as lex

reserved = {
   'float' : 'FLOATTYPE',
   'int'   : 'INTTYPE',
   'if'    : 'IF',
   'else'  : 'ELSE',
   'while' : 'WHILE',
   'print' : 'PRINT'
}

tokens = [
   'INTEGER',
   'FLOAT',
   'IDENTIFIER',
   'COMMA',
   'SEMICOLON',
   'PLUS',
   'MINUS',
   'MULT',
   'DIVIDE',
   'MOD',
   'LT',
   'LE',
   'GT',
   'GE',
   'NOT',
   'ISEQ',
   'ISNOTEQ',
   'OR',
   'AND',
   'LCURLYBRKT',
   'RCURLYBRKT',
   'LSQUAREBRKT',
   'RSQUAREBRKT',
   'LPAREN',
   'RPAREN',
   'ASSIGN'
] + list(reserved.values())

t_COMMA           = r','
t_SEMICOLON       = r';'
t_PLUS            = r'\+'
t_MINUS           = r'-'
t_MULT            = r'\*'
t_DIVIDE          = r'/'
t_MOD             = r'%'
t_LT              = r'\<'
t_LE              = r'<='
t_GT              = r'\>'
t_GE              = r'>='
t_NOT             = r'!'
t_ISEQ            = r'=='
t_ISNOTEQ         = r'!='
t_OR              = r'\|\|'
t_AND             = r'&&'
t_LCURLYBRKT      = r'\{'
t_RCURLYBRKT      = r'\}'
t_LSQUAREBRKT     = r'\['
t_RSQUAREBRKT     = r'\]'
t_LPAREN          = r'\('
t_RPAREN          = r'\)'
t_ASSIGN          = r'='
t_ignore          = ' \t'

def t_IDENTIFIER(t):
   r'[a-zA-Z_][0-9a-zA-Z]*' 
   t.type = reserved.get(t.value, 'IDENTIFIER')
   return t

def t_COMMENT(t):
   r'//.*\n'
   pass

def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

def t_FLOAT(t): 
   r'\d+\.\d*'
   t.value = float(t.value)
   return t

def t_INTEGER(t):
   r'\d+'
   t.value = int(t.value)
   return t

def t_error(t):
   print("Illegal character '%s'" % t.value)
   t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
   lex.runmain()
