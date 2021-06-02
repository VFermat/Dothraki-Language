from sly import Lexer


class DothLexer(Lexer):

    tokens = {PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN,
              RPAREN, BOPEN, BCLOSE, EOL, EQ, LE, LT, GE,
              GT, NE, AND, OR, TSTRING, TINT, VOID, BOOL, TFLOAT, NOT,
              IF, ELIF, ELSE, WHILE, RETURN, PRINT, NAME, NUMBER,
              FLOAT, STRING, TRUE, FALSE}
    ignore = ' \t,'
    literals = {'.', '!'}

    # Special Symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    BOPEN = r'\{'
    BCLOSE = r'\}'
    # EOL = r'(NAKHO)'
    EQ = r'=='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    AND = r'&&'
    NOT = r'!'
    OR = r'\|\|'

    # Variable Types
    # TSTRING = r'(ASE)'
    # TINT = r'(ATO)'
    # VOID = r'(SOM)'
    # BOOL = r'(TAWAK)'
    # TFLOAT = r'(NAQIS)'

    # Lexical Features
    # IF = r'(FIN)'
    # ELIF = r'(ESHNA)'
    # ELSE = r'(NAKHAAN)'
    # WHILE = r'(HAEI)'
    # RETURN = r'(EZAT)'
    # PRINT = r'(FREDRIK)'

    FLOAT = r'\d*\.?\d+'
    NUMBER = r'\d+'

    STRING = r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')'''

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['FIN'] = IF
    NAME['ESHNA'] = ELIF
    NAME['NAKHAAN'] = ELSE
    NAME['HAEI'] = WHILE
    NAME['EZAT'] = RETURN
    NAME['ASE'] = TSTRING
    NAME['ATO'] = TINT
    NAME['SOM'] = VOID
    NAME['TAWAK'] = BOOL
    NAME['NAQIS'] = TFLOAT
    NAME['NAKHO'] = EOL
    NAME['FREDRIK'] = PRINT
    NAME['taw'] = TRUE
    NAME['wat'] = FALSE

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
