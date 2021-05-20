from sly import Parser
from lexical import DothLexer


class DothParser(Parser):
    tokens = DothLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS, UNOT, UPLUS),
    )
    debugfile = 'parser.out'

    def __init__(self, debug=True):
        self.variables = {}

    @_('statement { statement }')
    def code(self, p):
        return 0

    @_(
        'command',
        'def_function'
    )
    def statement(self, p):
        return 0

    @_(
        'conditional',
        'loop',
        'declaration',
        'assignment',
        'returns',
        'call_function',
        'println',
        'or_expr',
    )
    def command(self, p):
        return 0

    @_(
        'TSTRING NAME LPAREN param { param } RPAREN block EOL',
        'TINT NAME LPAREN param { param } RPAREN block EOL',
        'TFLOAT NAME LPAREN param { param } RPAREN block EOL',
        'BOOL NAME LPAREN param { param } RPAREN block EOL',
    )
    def def_function(self, p):
        return 0

    @_(
        'IF LPAREN or_expr RPAREN block elseif',
        'IF LPAREN or_expr RPAREN block elses',
        'IF LPAREN or_expr RPAREN block EOL',
    )
    def conditional(self, p):
        return 0

    @_(
        'ELIF LPAREN or_expr RPAREN block elseif',
        'ELIF LPAREN or_expr RPAREN block elses',
        'ELIF LPAREN or_expr RPAREN block EOL',
    )
    def elseif(self, p):
        return 0

    @_('ELSE block EOL')
    def elses(self, p):
        return 0

    @_('WHILE LPAREN or_expr RPAREN block EOL')
    def loop(self, p):
        return 0

    @_(
        'TINT NAME ASSIGN or_expr EOL',
        'TSTRING NAME ASSIGN or_expr EOL',
        'BOOL NAME ASSIGN or_expr EOL',
        'TFLOAT NAME ASSIGN or_expr EOL',
        'TINT NAME EOL',
        'TSTRING NAME EOL',
        'BOOL NAME EOL',
        'TFLOAT NAME EOL',
    )
    def declaration(self, p):
        return 0

    @_('NAME ASSIGN or_expr EOL')
    def assignment(self, p):
        return 0

    @_('RETURN or_expr')
    def returns(self, p):
        return 0

    @_(
        'NAME LPAREN RPAREN EOL',
        'NAME LPAREN param { param } RPAREN EOL',
    )
    def call_function(self, p):
        return 0

    @_('PRINT LPAREN or_expr RPAREN EOL')
    def println(self, p):
        return 0

    @_(
        'TSTRING NAME',
        'TINT NAME',
        'TFLOAT NAME',
        'BOOL NAME',
    )
    def param(self, p):
        return 0

    @_('BOPEN command { command } BCLOSE')
    def block(self, p):
        return 0

    @_(
        'and_expr',
        'and_expr OR or_expr'
    )
    def or_expr(self, p):
        return 0

    @_(
        'eq_expr',
        'eq_expr AND and_expr'
    )
    def and_expr(self, p):
        return 0

    @_(
        'rel_expr',
        'rel_expr EQ eq_expr'
    )
    def eq_expr(self, p):
        return 0

    @_(
        'expr',
        'expr GT rel_expr',
        'expr LT rel_expr'
    )
    def rel_expr(self, p):
        return 0

    @_(
        'term',
        'term PLUS expr',
        'term MINUS expr'
    )
    def expr(self, p):
        return 0

    @_(
        'factor',
        'factor TIMES term',
        'factor DIVIDE term'
    )
    def term(self, p):
        return 0

    @_(
        'NUMBER',
        'PLUS factor %prec UPLUS',
        'MINUS factor %prec UMINUS',
        'NOT factor %prec UNOT',
        'LPAREN or_expr RPAREN',
        'NAME',
        'STRING',
        'FLOAT',
        'TRUE',
        'FALSE',
    )
    def factor(self, p):
        return 0
