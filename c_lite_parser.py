import ply.yacc as yacc
from c_lite_scanner import tokens
from ASTNode import BinaryOperation, \
UnaryOperation, IntegerConstant, FloatConstant, \
SingletonReference, ArrayReference, evaluate, \
execute, declare

def p_repl(p):
   '''program : exDeclarations 
              | exStatements
              | exPrint
              | exDeclarations exStatements'''
   pass

def p_exPrint(p):
   '''exPrint : PRINT expression SEMICOLON'''
   print(evaluate(p[2]))

def p_exDeclarations(p):
   '''exDeclarations : declarations'''
   for declaration in p[1]:
      declare(declaration)

def p_exStatements(p):
   '''exStatements : statements'''
   for statement in p[1]:
      execute(statement)

def p_declarations(p):
   '''declarations : declarations declaration
                   | declaration'''
   if len(p) == 3:
      p[0] = p[1] + p[2]
   else:
      p[0] = p[1]

def p_declaration(p):
   '''declaration : INTTYPE decparts SEMICOLON
                  | FLOATTYPE decparts SEMICOLON'''
   for decl in p[2]:
      decl['type'] = p[1] 
   p[0] = p[2]

def p_decparts(p):
   '''decparts : decparts COMMA decpart
               | decpart'''
   if len(p) == 4:
      p[0] = p[1] + p[3]
   else: 
      p[0] = p[1]

def p_decpart(p):
   '''decpart : IDENTIFIER
              | IDENTIFIER LSQUAREBRKT INTEGER RSQUAREBRKT'''
   if len(p) == 2:
      p[0] = [{'name' : p[1], 'isArray' : False, 'length' : 0, 'value' : None}]
   else: 
      p[-1] = [{'name' : p[1], 'isArray' : True, 'length' : p[3], 'value' : [None for i in range(p[3])]}]

def p_statements(p):
   '''statements : statements statement
                 | statement'''
   if len(p) == 3:
      p[0] = p[1] + p[2]
   else: 
      p[0] = p[1]

def p_statement(p):
   '''statement : SEMICOLON
                | block
                | assignment
                | ifStatement
                | whileStatement'''
   if p[1] == ';':
      p[0] = []
   else:
      p[0] = p[1]

def p_block(p):
   '''block : LCURLYBRKT statements RCURLYBRKT'''
   p[0] = p[2]

def p_assignment(p):
   '''assignment : IDENTIFIER ASSIGN expression SEMICOLON
                 | IDENTIFIER LSQUAREBRKT expression RSQUAREBRKT ASSIGN expression SEMICOLON'''
   if len(p) == 5:
      p[0] = [{'type' : 'assign', 'lhs' : SingletonReference(p[1]), 'rhs' : evaluate(p[3])}]
   else:
      p[0] = [{'type' : 'assign', 'lhs' : ArrayReference(p[1], evaluate(p[3])), 'rhs' : evaluate(p[6])}]

def p_ifStatement(p):
   '''ifStatement : IF LPAREN expression RPAREN statement
                  | IF LPAREN expression RPAREN statement ELSE statement'''
   if len(p) == 6:
      p[0] = [{'type' : 'if', 'condition' : evaluate(p[3]), 'ifPart' : p[5]}]
   else:
      p[0] = [{'type' : 'ifelse', 'condition' : evaluate(p[3]), 'ifPart' : p[5], 'elsePart' : p[7]}]

def p_whileStatement(p):
   '''whileStatement : WHILE LPAREN expression RPAREN statement'''
   p[0] = [{'type' : 'while', 'condition' : evaluate(p[3]), 'whilePart' : p[5]}]

def p_expression(p):
   '''expression : conjunctions'''
   p[0] = p[1]
 
def p_conjunctions(p):
   '''conjunctions : conjunctions OR conjunction
                   | conjunction''' 
   if len(p) == 4:
      p[0] = BinaryOperation(p[1], p[2], p[3])
   else:
      p[0] = p[1]

def p_conjunction(p):
   '''conjunction : equalities'''
   p[0] = p[1]

def p_equalities(p):
   '''equalities : equalities AND equality
                 | equality'''
   if len(p) == 4:
      p[0] = BinaryOperation(p[1], p[2], p[3])
   else:
      p[0] = p[1]
   
def p_equality(p):
   '''equality : relation ISEQ relation
               | relation ISNOTEQ relation
               | relation'''
   if len(p) == 4:
      p[0] = BinaryOperation(p[1], p[2], p[3])
   else:
      p[0] = p[1]

def p_relation(p):
   '''relation :  addition LT addition
                | addition LE addition
                | addition GT addition
                | addition GE addition
                | addition'''
   if len(p) == 4:
      p[0] = BinaryOperation(p[1], p[2], p[3])
   else:
      p[0] = p[1]

def p_addition(p):
   '''addition : terms'''
   p[0] = p[1]

def p_terms(p):
   '''terms : terms PLUS term
            | terms MINUS term
            | term'''
   if len(p) == 4:
      p[0] = BinaryOperation(p[1], p[2], p[3])
   else:
      p[0] = p[1]

def p_term(p):
   '''term : factors'''
   p[0] = p[1]

def p_factors(p):
   '''factors : factors MULT factor
              | factors DIVIDE factor
              | factors MOD factor
              | factor'''
   if len(p) == 4:
      p[0] = BinaryOperation(p[1], p[2], p[3])
   else:
      p[0] = p[1]

def p_factor(p):
   '''factor : primary
             | NOT primary'''  
   if len(p) == 2:
      p[0] = p[1]
   else:
      p[0] = UnaryOperation(p[1], p[2])

def p_primary(p):
   '''primary : IDENTIFIER
              | IDENTIFIER LSQUAREBRKT expression RSQUAREBRKT 
              | literal
              | LPAREN expression RPAREN'''
   if len(p) == 2: # identifier and literal case
      if isinstance(p[1], IntegerConstant) or isinstance(p[1], FloatConstant):
         p[0] = p[1]
      else: # identifier
         p[0] = SingletonReference(p[1])
   elif len(p) == 4: # paren case
      p[0] = p[2]
   else: #the array case
      p[0] = ArrayReference(p[1], execute(p[3]).value)

def p_literal(p):
   '''literal : INTEGER
              | FLOAT'''
   if isinstance(p[1], int):
      p[0] = IntegerConstant(p[1])
   else:
      p[0] = FloatConstant(p[1])

def p_error(p):
   print('syntax error')
              
parser = yacc.yacc()

while True:
   try:
      s = input('C Lite Iterpreter> ')
   except EOFError:
      break
   if not s: continue
   parser.parse(s)
