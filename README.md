# C_Lite_Interpreter

In this program, we used PLY ( Python Lex-Yacc)

 In a nutshell, PLY is nothing more than a straightforward lex/yacc implementation. Here is a list of its essential features:

     --It's implemented entirely in Python.

     --It uses LR-parsing which is reasonably efficient and well suited for larger grammars.

     --PLY provides most of the standard lex/yacc features including support for empty productions, precedence rules, error    
       recovery, and support for ambiguous grammars.

     --PLY is straightforward to use and provides very extensive error checking.

     --PLY doesn't try to do anything more or less than provide the basic lex/yacc functionality. In other words, it's not a 
       large parsing framework or a component of some larger system. 
      
So, we have used python for this project, which all work in conjunction to process user input. The program accepts one line input, so input can be givin line by line. However, if the int is declared in one line, and then initialized in another line, the program will match the input. The input must end in a semicolon inorder to be counted. 

The three files included in this project are following:

    -- ASTNode.py -> 
      --- This declares all the types that will be expected, lifke Integers, floats, binary operations, unary operations,    
          singleton references, adn arrary references. 
      --- This declares the symbol_table  (symbol_table = dict()) that hold self.info about various types. 
      --- This contains the typechecking system checking left hand delcartions to its right. 
     
    -- c_lite_scanner.py ->
      ---This scans user input and tokenizes it into ASTNode defintions and passes those tokens to the parser. The following      
         is the list of tokens.
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
       --- This contains defintions of the types the input can me: Identifier, comment, newline, float, integer, error.
       --- Calls lex.runmain()
  
    -- c_lite_parser.py ->
       --- This takes the tokens and determines the grammatic validity of the tokens. 
       --- This defines the grammar rules usded to determine the graammatic validity of the token. The grammar rules were   
           referenced from the book: Programming Language: Principles and Paradigms (Tucker).
       --- Writes three types of errors. 
               TypeError -> type mismatch
               KeyError -> name does not exist
               IndexError -> index out of range
     
  The program was tested with the provided postive and negative test cases. 
  
  The following Postive_Test_Cases were entered line by line and passed the program without any error.
  
                      int a,b,c,d;
                      float e,f,g,h;
                      int i[3];

                      a = 1 + 2;
                      b = 2 * 3;
                      c = 4 / 2;
                      d = 2 - 1;


                      e = 1.5 + 2.5;
                      f = 2.5 * 2.0;
                      g = 4.0 / 2.0;
                      h = 3.5 - 1.5;


                      i[0] = 1;
                      i[1] = 2;
                      i[2] = i[0] + i[1];

                      if(1){a = 3;}

                      if(0){i[1] = 1;}else{i[1] = i[2];}

The following Negative_Test_Cases were entered line by line and produced errors.

                      int a,b,c,d; 
                      float e,f,g,h; 
                      int i[3]; 

                      a =  + ; 
                      b = 2 * ; 
                      c =  / 2;
                      d = 2 - ;


                      e = + 2.5;
                      f = 2.5 * ;
                      g = / ;
                      h = 


                      i[0] = 1
                      i[1] = 2;
                      i[2] = i[0]  i[1];

                      if(){
                          a = 3;
                      }

                      if(0){
                          i[1] = 1;

                      else{
                          i[1] = i[2];

  
     

# References
+ http://epaperpress.com/lexandyacc/download/LexAndYaccTutorial.pdf
+ http://www.dabeaz.com/ply/ply.html
+ http://memphis.compilertools.net/interpreter.html
+ Programming Language: Principles and Paradigms (Tucker)
