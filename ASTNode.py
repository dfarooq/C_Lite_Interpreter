symbol_table = dict()

class ASTNode: pass
   
class BinaryOperation(ASTNode):
   def __init__(self, left, op, right):
      self.type = 'binary operation'
      self.left = left
      self.right = right
      self.op = op

class UnaryOperation(ASTNode):
   def __init__(self, op, term):
      self.type = 'unary operation'
      self.op = op
      self.term = term

class IntegerConstant(ASTNode):
   def __init__(self, value):
      self.type = 'int constant'
      self.value = value

class FloatConstant(ASTNode):
   def __init__(self, value):
      self.type = 'float constant'
      self.value = value

class SingletonReference(ASTNode):
   def __init__(self, name):
      self.type = 'singleton reference'
      self.name = name
      self.info = symbol_table[name]

class ArrayReference(ASTNode):
   def __init__(self, name, index):
      self.type = 'array reference' 
      self.name = name
      self.info = symbol_table[name]
      self.index = index

def makeType(val, typeOf):
   if typeOf == 'float':
      return float(val)
   else: 
      return int(val)

def evaluate(root):
   if not root: 
      return 0

   if root.type == 'int constant': 
      return root.value

   elif root.type == 'float constant':
      return root.value
   
   elif root.type == 'singleton reference':
      return root.info['value']

   elif root.type == 'array reference': 
      return root.info['value'][root.index]

   elif root.type == 'unary operation':
      if root.op == '!':
         return not root.term

   else: #binary operation ! 
      lhs = evaluate(root.left)
      rhs = evaluate(root.right)

      # type checking system
      if type(lhs) != type(rhs):
         raise TypeError

      typeOf = type(lhs).__name__
      if root.op == '||':
         return makeType((lhs or rhs), typeOf)

      if root.op == 'and':
         return makeType((lhs and rhs), typeOf)
 
      if root.op == '==':
         return makeType((lhs == rhs), typeOf)

      if root.op == '!=':
         return makeType((lhs != rhs), typeOf)

      if root.op == '<':
         return makeType((lhs < rhs), typeOf)

      if root.op == '<=':
         return makeType((lhs <= rhs), typeOf)

      if root.op == '>':
         return makeType((lhs > rhs), typeOf)

      if root.op == '>=':
         return makeType((lhs >= rhs), typeOf)

      if root.op == '+': 
         return makeType((lhs + rhs), typeOf)

      if root.op == '-':
         return makeType((lhs - rhs), typeOf)

      if root.op == '*':
         return makeType((lhs * rhs), typeOf)

      if root.op == '/':
         return makeType((lhs / rhs), typeOf)

      if root.op == '%':
         return makeType((lhs % rhs), typeOf)

def declare(declaration):
   name = declaration.pop('name', None)
   symbol_table[name] = declaration 

def execute(statement):
   if statement['type'] == 'assign':
      lhs = statement['lhs']
      rhs = statement['rhs']

      if lhs.info['type'] != type(rhs).__name__:
         raise TypeError

      if isinstance(lhs, SingletonReference):
         symbol_table[lhs.name]['value'] = rhs
          
      else: # ArrayReference
         symbol_table[lhs.name]['value'][lhs.index] = rhs

   ## if statement
   if statement['type'] == 'if':
     if statement['condition']: 
        for s in statement['ifPart']:
           execute(s)
   
   # if-else statement
   if statement['type'] == 'ifelse':
      if statement['condition']:
         for s in statement['ifPart']:
            execute(s)
      else: 
         for s in statement['elsePart']:
            execute(s)

   # while statement
   if statement['type'] == 'while':
      while statement['condition']:
         print(statement['condition'])
         for s in statement['whilePart']:
            execute(s)
