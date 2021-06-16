import sys
sys.path.append('../')
from typing import List, NoReturn, Union, Set
from sly.lex import Token
from helpers.symbolTable import SymbolTable
from llvmlite import ir
import uuid
from copy import deepcopy


class Node:

    module = None
    builder = None
    printf = None
    printfFmtArg = None

    def __init__(self, value: Token):
        self.value = value
        self.children: List[Node] = []
        self.id = str(uuid.uuid4())

    def evaluate(self, table: SymbolTable) -> int:
        return 0


class Block(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def addChild(self, child: Node) -> NoReturn:
        self.children.append(child)

    def evaluate(self, table) -> NoReturn:
        for child in self.children:
            child.evaluate(table)


class DefFuncOp(Node):

    type_dict = {
        'TINT': ir.IntType(32),
        'TFLOAT': ir.FloatType(),
        'TSTRING': ir.ArrayType(ir.IntType(8), 64),
        'BOOL': ir.IntType(1),
        'VOID': ir.VoidType(),
    }
    var_dict = {
        'TINT': 'int',
        'TFLOAT': 'float',
        'TSTRING': 'string',
        'BOOL': 'bool',
        'VOID': 'void',
    }

    def __init__(self, value: Token, funcType: Token):
        super().__init__(value)
        self.params = []
        self.block = None
        self.funcType = self.type_dict[funcType.type]

    def addParam(self, param: List):
        param = [param[0].type, param[1].value]
        self.params.append(param)

    def setBlock(self, block: Node):
        self.block = block

    def evaluate(self, table: SymbolTable):
        fnty = ir.FunctionType(
            self.funcType, [self.type_dict[p[0]] for p in self.params])
        func = ir.Function(self.module, fnty, name=self.value.value)

        funcBlock = func.append_basic_block(f'{self.value.value}_entry')
        previousBuilder = self.builder

        Node.builder = ir.IRBuilder(funcBlock)

        paramsPtrs = []
        for i, typ in enumerate([self.type_dict[p[0]] for p in self.params]):
            ptr = self.builder.alloca(typ)
            self.builder.store(func.args[i], ptr)
            paramsPtrs.append(ptr)

        scopeTable = SymbolTable()
        for i, (typ, name) in enumerate(self.params):
            scopeTable.declareVariable(
                name, paramsPtrs[i])

        for var, val in table.table.items():
            if val['type'] == 'function':
                scopeTable.declareVariable(var, val['pointer'], val['type'])

        scopeTable.declareVariable(self.value.value, func)
        self.block.evaluate(scopeTable)
        if self.funcType == ir.VoidType():
            self.builder.ret_void()

        table.declareVariable(self.value.value, func, "function")
        Node.builder = previousBuilder
        return table


class IfOp(Node):

    condition: Node
    commandTrue: Node
    commandElse: Node
    elifClauses: List[List[Node]]

    def __init__(self, value: Token, condition: Node, commandTrue: Node):
        super().__init__(value)
        self.condition = condition
        self.commandTrue = commandTrue
        self.commandElse = None
        self.elifClauses = []

    def setElse(self, commandElse: Node) -> NoReturn:
        self.commandElse = commandElse

    def addElif(self, clause: Node, command: Node) -> NoReturn:
        self.elifClauses.append([clause, command])

    def evaluate(self, table: SymbolTable) -> NoReturn:
        cond = self.condition.evaluate(table)
        with self.builder.if_else(cond) as (then, otherwise):
            with then:
                self.commandTrue.evaluate(table)
            with otherwise:
                if self.commandElse:
                    self.commandElse.evaluate(table)


class LoopOp(Node):

    condition: Node
    command: Node

    def __init__(self, value: Token, condition: Node, command: Node):
        super().__init__(value)
        self.condition = condition
        self.command = command

    def evaluate(self, table: SymbolTable) -> NoReturn:
        loopEntry = self.builder.append_basic_block(name=f"while_{self.id}")
        loopOut = self.builder.append_basic_block(name=f"while_out_{self.id}")
        cond = self.condition.evaluate(table)
        self.builder.cbranch(cond, loopEntry, loopOut)
        pos = self.builder.position_at_start(loopEntry)
        com = self.command.evaluate(table)
        cond = self.condition.evaluate(table)
        self.builder.cbranch(cond, loopEntry, loopOut)
        self.builder.position_at_start(loopOut)


class DeclarationOp(Node):

    var_type: Token
    expr: Node
    var_dict = {
        'TINT': ir.IntType(32),
        'TFLOAT': ir.FloatType(),
        'TSTRING': ir.ArrayType(ir.IntType(8), 64),
        'BOOL': ir.IntType(1),
        'VOID': ir.VoidType(),
    }

    def __init__(self, value: Token, var_type: Token, expr: Node):
        super().__init__(value)
        self.var_type = self.var_dict[var_type.type]
        self.expr = expr

    def evaluate(self, table: SymbolTable):
        expr = self.expr.evaluate(table)
        irAloc = self.builder.alloca(self.var_type, name=self.value.value)
        self.builder.store(expr, irAloc)
        table.declareVariable(self.value.value, irAloc)
        return table


class AssignmentOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table: SymbolTable):
        pointer, tmp = table.getVariable(self.value.value)
        expr = self.expr.evaluate(table)
        self.builder.store(expr, pointer)
        table.setVariable(self.value.value, pointer)
        return table


class ReturnOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table):
        return self.builder.ret(self.expr.evaluate(table))


class CallFunOp(Node):

    expr: Node
    params: List[Node]

    def __init__(self, value: Token, params: List[Node]):
        super().__init__(value)
        self.params = params

    def evaluate(self, table):
        args = []
        for param in self.params:
            value = param.evaluate(table)
            args.append(value)

        func, tmp = table.getVariable(self.value)
        ret = self.builder.call(func, args)
        return ret


class PrintOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table):
        value = self.expr.evaluate(table)
        # value = self.builder.trunc(value, ir.IntType(8))
        globalFmt, voidptrY = self.printfFmtArg

        strFmt = self.builder.bitcast(globalFmt, voidptrY)
        # Call Print Function
        self.builder.call(self.printf, [strFmt, value])


class BinOp(Node):

    def __init__(self, value: Token, left: Node, right: Node):
        super().__init__(value)
        self.children = [left, right]

    def evaluate(self, table: SymbolTable):
        children0 = self.children[0].evaluate(table)
        children1 = self.children[1].evaluate(table)
        if self.value.type == 'PLUS':
            i = self.builder.add(children0, children1)
        elif self.value.type == 'MINUS':
            i = self.builder.sub(children0, children1)
        elif self.value.type == 'TIMES':
            i = self.builder.mul(children0, children1)
        elif self.value.type == 'DIVIDE':
            i = self.builder.sdiv(children0, children1)
        elif self.value.type == 'EQ':
            i = self.builder.icmp_signed('==', children0, children1)
        elif self.value.type == 'NE':
            i = self.builder.icmp_signed('!=', children0, children1)
        elif self.value.type == 'OR':
            i = self.builder.or_(children0, children1)
        elif self.value.type == 'AND':
            i = self.builder.and_(children0, children1)
        elif self.value.type == 'GT':
            i = self.builder.icmp_signed('>', children0, children1)
        elif self.value.type == 'GE':
            i = self.builder.icmp_signed('>=', children0, children1)
        elif self.value.type == 'LT':
            i = self.builder.icmp_signed('<', children0, children1)
        elif self.value.type == 'LE':
            i = self.builder.icmp_signed('<=', children0, children1)
        else:
            raise BufferError(f"Invalid operation of type {self.value.type}")
        return i


class UnOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table):
        ret = self.expr.evaluate(table)
        if self.value.type == 'UPLUS' or self.value.type == 'PLUS':
            return ret
        elif self.value.type == 'UMINUS' or self.value.type == 'MINUS':
            return self.builder.neg(ret)
        elif self.value.type == 'UNOT' or self.value.type == 'NOT':
            return self.builder.not_(ret)
        else:
            raise BufferError(f"Invalid operation of type {self.value.type}")


class IntVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return ir.Constant(ir.IntType(32), self.value.value)


class FloatVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        if '.' in self.value.value:
            return ir.Constant(ir.FloatType(), self.value.value)
        return ir.Constant(ir.IntType(32), self.value.value)


class StringVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        i = ir.Constant(ir.ArrayType(ir.IntType(8), 64),
                        bytearray(self.value.value.encode("utf8") + (" "*(64 - len(self.value.value))).encode("utf8")))
        return i


class BoolVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return ir.Constant(ir.IntType(1), self.value.value)


class IdentifierVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        variable, tmp = table.getVariable(self.value.value)
        i = self.builder.load(variable, name=self.value.value)
        return i


class NoOp(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return ir.Constant(ir.IntType(32), 0)
