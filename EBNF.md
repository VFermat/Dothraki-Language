```
CODE = {STATEMENT};
STATEMENT = FUNCTION | CONDITIONAL | LOOP | ASSIGNMENT | RETURN;
S_STATEMENT = IDENTIFIER | NUMBER | STRING | EXPRESSION;

IDENTIFIER = LETTER, {LETTER, DIGIT, "_"};

FUNCTION = "ATAKI", VTYPE, IDENTIFIER, "(", [{PARAM}], ")", BLOCK, "NAKHO";

CONDITIONAL = "ATAKI", "FIN", "(", COMPARISSON, ")", BLOCK, ELSEIF |
            "ATAKI", "FIN", "(", COMPARISSON, ")", BLOCK, ELSE |
            "ATAKI", "FIN", "(", COMPARISSON, ")", BLOCK, "NAKHO";

ELSEIF = "ESHNA", "(", COMPARISSON, ")", BLOCK, ELSEIF |
        "ESHNA", "(", COMPARISSON, ")", BLOCK, ELSE |
        "ESHNA", "(", COMPARISSON, ")", BLOCK, "NAKHO";

ELSE = "NAKHAAN", "(", COMPARISSON, ")", BLOCK, "NAKHO";

LOOP : "ATAKI", "HAEI", "(", COMPARISSON, ")", BLOCK, "NAKHO";

ASSIGNMENT = VTYPE, IDENTIFIER, "=", (S_STATEMENT), "NAKHO";

RETURN = "EZAT", (S_STATEMENT);

BLOCK = "{", {STATEMENT}, "}";

COMPARISSON = EXPRESSION, COMPARATORS, EXPRESSION;

PARAM = VTYPE, IDENTIFIER;
VTYPE = "ASE" | "ATO" | "SOM" | "TAWAK" | "NAQIS";

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
WORD = LETTER, {LETTER};

COMPARATORS = ">" | "<" | ">=" | "<=" | "==" | "!=";
```

## Variable Types

- ASE -> String
- ATO -> Integer
- SOM -> Void
- TAWAK -> Boolean
- NAQIS -> Float

## Lexical Features

- ATAKI -> Start of command
- NAKHO -> End of statement/line
- FIN -> If
- ESHNA -> Else if
- NAKHAAN -> Else
- HAEI -> While
- EZAT -> Return
