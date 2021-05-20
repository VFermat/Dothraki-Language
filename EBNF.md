## Doth Lang EBNF

```
code = statement, {statement};
statement = def_function | command;

def_function = vtype, IDENTIFIER, "(", param, {",", param}, ")", block, "NAKHO";

command = conditional | loop | declaration |
          assignment | returns | call_function |
          println | or_expr;

conditional = "FIN", "(", or_expr, ")", block, elseif |
            "FIN", "(", or_expr, ")", block, else |
            "FIN", "(", or_expr, ")", block, "NAKHO";

elseif = "ESHNA", "(", or_expr, ")", block, elseif |
        "ESHNA", "(", or_expr, ")", block, else |
        "ESHNA", "(", or_expr, ")", block, "NAKHO";

else = "NAKHAAN", block, "NAKHO";

loop = "HAEI", "(", or_expr, ")", block, "NAKHO";

declaration = vtype, IDENTIFIER, ASSIGN, or_expr, "NAKHO" |
             vtype, IDENTIFIER, "NAKHO";

assignment = IDENTIFIER, ASSIGN, or_expr, "NAKHO";

returns = "EZAT", or_expr;

call_function = IDENTIFIER, "(", {",", param}, ")", "NAKHO";

println = "FREDRIK", "(", or_expr ")", "NAKHO";

param = vtype, IDENTIFIER;

IDENTIFIER = LETTER, {LETTER, DIGIT, "_"};

block = "{", command, {command}, "}";

or_expr = and_expr | and_expr, OR, or_expr;

and_expr = eq_expr | eq_expr, AND, and_expr;

eq_expr = rel_expr | rel_expr, EQ, eq_expr;

rel_expr = expr | expr, GT, rel_expr | expr, LT, rel_expr;

expr = term | term, PLUS, expr | term, MINUS, expr;

term = factor | factor, TIMES, term | factor, DIVIDE, term;

factor = NUMBER | PLUS, factor | MINUS, factor |
        NOT, factor | "(", or_expr, ")" | IDENTIFIER |
        STRING | FLOAT | TRUE | FALSE;

vtype = "ASE" | "ATO" | "SOM" | "TAWAK" | "NAQIS";

PLUS = "+";
MINUS = "-";
TIMES = "*";
NOT = "!";
AND = "&&";
OR = "||";
EQ = "==";
GT = ">";
LT = "<";

DIGIT = 0 | 1 | 2 | 3
        4 | 5 | 6
        7 | 8 | 9;
NUMBER = DIGIT, {DIGIT};

LETTER = "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z" ;

CHAR = DIGIT | LETTER | " " | "_" | "-" | PLUS |
        MINUS | TIMES | NOT | AND | OR | EQ | GT |
        LT | "?";

STRING = """, {char}, """;

TRUE = "taw";
FALSE = "wat";
```
