import sys
sys.path.append('../')
from sly import Parser
from compiler.lexical import DothLexer
from helpers.nodes import Node, Block, DefFuncOp, IfOp, LoopOp, DeclarationOp, AssignmentOp, ReturnOp, CallFunOp, PrintOp, BinOp, UnOp, IntVal, FloatVal, StringVal, BoolVal, IdentifierVal, NoOp
from llvmlite import ir


class DothParser(Parser):
    tokens = DothLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS, UNOT, UPLUS),
    )
    debugfile = './out/parser.out'

    def __init__(self, module, builder, printf, debug=True):
        self.module = module
        self.builder = builder
        self.printf = printf
        self.variables = {}
        Node.module = self.module
        Node.builder = self.builder
        Node.printf = self.printf
        Node.printfFmtArg = self._configurePrintf()

    def _configurePrintf(self):
        # Declare argument list
        voidptrY = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        cFmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                           bytearray(fmt.encode("utf8")))
        globalFmt = ir.GlobalVariable(self.module, cFmt.type, name="fstr")
        globalFmt.linkage = 'internal'
        globalFmt.global_constant = True
        globalFmt.initializer = cFmt
        return globalFmt, voidptrY

    @_('{ statement }')
    def code(self, p):
        root = Block(None)
        for stat in p.statement:
            root.addChild(stat)
        return root

    @_(
        'command',
        'def_function'
    )
    def statement(self, p):
        values = p._slice
        if values[0].type == 'command':
            return p.command
        else:
            return p.def_function

    @_(
        'conditional',
        'loop',
        'declaration',
        'assignment',
        'returns',
        'println',
        'or_expr',
    )
    def command(self, p):
        values = p._slice
        if values[0].type == 'conditional':
            return p.conditional
        elif values[0].type == 'loop':
            return p.loop
        elif values[0].type == 'declaration':
            return p.declaration
        elif values[0].type == 'assignment':
            return p.assignment
        elif values[0].type == 'returns':
            return p.returns
        elif values[0].type == 'println':
            return p.println
        elif values[0].type == 'or_expr':
            return p.or_expr
        return values[0]

    @_(
        'TSTRING NAME LPAREN RPAREN block EOL',
        'TSTRING NAME LPAREN param { COMMA param } RPAREN block EOL',
        'TINT NAME LPAREN RPAREN block EOL',
        'TINT NAME LPAREN param { COMMA param } RPAREN block EOL',
        'TFLOAT NAME LPAREN RPAREN block EOL',
        'TFLOAT NAME LPAREN param { COMMA param } RPAREN block EOL',
        'BOOL NAME LPAREN RPAREN block EOL',
        'BOOL NAME LPAREN param { COMMA param } RPAREN block EOL',
        'VOID NAME LPAREN RPAREN block EOL',
        'VOID NAME LPAREN param { COMMA param } RPAREN block EOL',
    )
    def def_function(self, p):
        values = p._slice
        if len(values) > 6:
            params = [p.param0] + p.param1
        else:
            params = []
        func = DefFuncOp(values[1], values[0])
        for prm in params:
            func.addParam(prm)
        func.setBlock(p.block)
        return func

    @_(
        'IF LPAREN or_expr RPAREN block elseif',
        'IF LPAREN or_expr RPAREN block elses',
        'IF LPAREN or_expr RPAREN block EOL',
    )
    def conditional(self, p):
        values = p._slice
        if values[-1].type == 'EOL':
            return IfOp(values[0], p.or_expr, p.block)
        elif values[-1].type == 'elses':
            root = IfOp(values[0], p.or_expr, p.block)
            elses = p.elses
            root.setElse(elses)
            return root
        elif values[-1].type == 'elseif':
            root = IfOp(values[0], p.or_expr, p.block)
            elifs = p.elseif
            root.setElse(elifs)
            return root

    @_(
        'ELIF LPAREN or_expr RPAREN block elseif',
        'ELIF LPAREN or_expr RPAREN block elses',
        'ELIF LPAREN or_expr RPAREN block EOL',
    )
    def elseif(self, p):
        values = p._slice
        root = IfOp(values[0], p.or_expr, p.block)
        if values[-1].type == 'EOL':
            return root
        elif values[-1].type == 'elseif':
            elif_ = p.elifs
            root.setElse(elif_)
            return root
        elif values[-1].type == 'elses':
            else_ = p.elses
            root.setElse(else_)
            return root

    @_('ELSE block EOL')
    def elses(self, p):
        return p.block

    @_('WHILE LPAREN or_expr RPAREN block EOL')
    def loop(self, p):
        return LoopOp(p.WHILE, p.or_expr, p.block)

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
        values = p._slice
        if len(values) > 3:
            return DeclarationOp(values[1], values[0], p.or_expr)
        else:
            return DeclarationOp(values[1], values[0], NoOp(values[0]))

    @_('NAME ASSIGN or_expr EOL')
    def assignment(self, p):
        values = p._slice
        return AssignmentOp(values[0], p.or_expr)

    @_('RETURN or_expr EOL')
    def returns(self, p):
        return ReturnOp(p.RETURN, p.or_expr)

    @_(
        'NAME LPAREN RPAREN',
        'NAME LPAREN or_expr { COMMA or_expr } RPAREN',
    )
    def call_function(self, p):
        values = p._slice
        if len(values) > 3:
            or_exprs = [p.or_expr0] + p.or_expr1
            return CallFunOp(p.NAME, or_exprs)
        return CallFunOp(p.NAME, [])


    @_('PRINT LPAREN or_expr RPAREN EOL')
    def println(self, p):
        return PrintOp(p.PRINT, p.or_expr)

    @_(
        'TSTRING NAME',
        'TINT NAME',
        'TFLOAT NAME',
        'BOOL NAME',
    )
    def param(self, p):
        values = p._slice
        return values[0], values[1]

    @_('BOPEN { command } BCLOSE')
    def block(self, p):
        values = p._slice
        root = Block(values[0])
        for cmd in p.command:
            root.addChild(cmd)
        return root

    @_(
        'and_expr',
        'and_expr OR or_expr'
    )
    def or_expr(self, p):
        values = p._slice
        if len(values) > 1:
            return BinOp(values[1], p.and_expr, p.or_expr)
        else:
            return p.and_expr

    @_(
        'eq_expr',
        'eq_expr AND and_expr'
    )
    def and_expr(self, p):
        values = p._slice
        if len(values) > 1:
            return BinOp(values[1], p.eq_expr, p.and_expr)
        else:
            return p.eq_expr

    @_(
        'rel_expr',
        'rel_expr EQ eq_expr',
        'rel_expr NE eq_expr'
    )
    def eq_expr(self, p):
        values = p._slice
        if len(values) > 1:
            return BinOp(values[1], p.rel_expr, p.eq_expr)
        else:
            return p.rel_expr

    @_(
        'expr',
        'expr GT rel_expr',
        'expr LT rel_expr',
        'expr GE rel_expr',
        'expr LE rel_expr'
    )
    def rel_expr(self, p):
        values = p._slice
        if len(values) > 1:
            return BinOp(values[1], p.expr, p.rel_expr)
        else:
            return p.expr

    @_(
        'term',
        'term PLUS expr',
        'term MINUS expr'
    )
    def expr(self, p):
        values = p._slice
        if len(values) > 1:
            return BinOp(values[1], p.term, p.expr)
        else:
            return p.term

    @_(
        'factor',
        'factor TIMES term',
        'factor DIVIDE term'
    )
    def term(self, p):
        values = p._slice
        if len(values) > 1:
            return BinOp(values[1], p.factor, p.term)
        else:
            return p.factor

    @_(
        'NUMBER',
        'PLUS factor %prec UPLUS',
        'MINUS factor %prec UMINUS',
        'NOT factor %prec UNOT',
        'LPAREN or_expr RPAREN',
        'NAME',
        'STRING',
        'FLOAT',
        'call_function',
        'TRUE',
        'FALSE',
    )
    def factor(self, p):
        values = p._slice
        if values[0].type == 'NUMBER':
            return IntVal(values[0])
        elif values[0].type in ['PLUS', 'MINUS', 'NOT']:
            return UnOp(values[0], p.factor)
        elif values[0].type == 'NAME':
            return IdentifierVal(values[0])
        elif values[0].type == 'STRING':
            return StringVal(values[0])
        elif values[0].type == 'FLOAT':
            return FloatVal(values[0])
        elif values[0].type in ['TRUE', 'FALSE']:
            return BoolVal(values[0])
        elif values[0].type == 'call_function':
            return p.call_function
