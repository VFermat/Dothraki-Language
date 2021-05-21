from typing import List, NoReturn, Union, Set
from sly.lex import Token
from symbolTable import SymbolTable


class Node:
    def __init__(self, value: Token):
        self.value = value
        self.children: List[Node] = []

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

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table):
        return 0


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
        if self.condition.evaluate(table)[0]:
            self.commandTrue.evaluate(table)
        else:
            for clause in self.elifClauses:
                if clause[0].evaluate(table)[0]:
                    clause[1].evaluate(table)
                    return
            if self.commandElse != None:
                self.commandElse.evaluate(table)


class LoopOp(Node):

    condition: Node
    command: Node

    def __init__(self, value: Token, condition: Node, command: Node):
        super().__init__(value)
        self.condition = condition
        self.command = command

    def evaluate(self, table: SymbolTable) -> NoReturn:
        while self.condition.evaluate(table)[0]:
            self.command.evaluate(table)


class DeclarationOp(Node):

    var_type: Token
    expr: Node
    var_dict = {
        'TINT': 'int',
        'TFLOAT': 'float',
        'TSTRING': 'string',
        'BOOL': 'bool',
    }

    def __init__(self, value: Token, var_type: Token, expr: Node):
        super().__init__(value)
        self.var_type = self.var_dict[var_type.type]
        self.expr = expr

    def evaluate(self, table: SymbolTable):
        table.declareVariable(
            self.value.value, self.expr.evaluate(table)[0], self.var_type)
        return table


class AssignmentOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table: SymbolTable):
        expr = self.expr.evaluate(table)
        table.setVariable(self.value.value,
                          expr[0], expr[1])
        return table


class ReturnOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table):
        return self.expr.evaluate(table)


class CallFunOp(Node):

    expr: Node
    params: List[Node]

    def __init__(self, value: Token, params: List[Node]):
        super().__init__(value)
        self.params = params

    def evaluate(self, table):
        return super().evaluate(table)


class PrintOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table):
        print(self.expr.evaluate(table)[0])


class BinOp(Node):

    def __init__(self, value: Token, left: Node, right: Node):
        super().__init__(value)
        self.children = [left, right]

    def evaluate(self, table: SymbolTable):
        children0 = self.children[0].evaluate(table)
        children1 = self.children[1].evaluate(table)
        operation_result = None
        var_type = None
        if self.value.type == 'PLUS':
            operation_result = children0[0] + children1[0]
            if children0[1] == 'int' and children1[1] == 'int':
                var_type = 'int'
            elif 'float' in [children0[1], children1[1]]:
                var_type = 'float'
        elif self.value.type == 'MINUS':
            operation_result = children0[0] - children1[0]
            if children0[1] == 'int' and children1[1] == 'int':
                var_type = 'int'
            elif 'float' in [children0[1], children1[1]]:
                var_type = 'float'
        elif self.value.type == 'TIMES':
            operation_result = children0[0] * children1[0]
            if children0[1] == 'int' and children1[1] == 'int':
                var_type = 'int'
            elif 'float' in [children0[1], children1[1]]:
                var_type = 'float'
        elif self.value.type == 'DIVIDE':
            operation_result = children0[0] / children1[0]
            var_type = "float"
        elif self.value.type == 'EQ':
            operation_result = children0[0] == children1[0]
            var_type = "bool"
        elif self.value.type == 'OR':
            operation_result = children0[0] or children1[0]
            var_type = "bool"
        elif self.value.type == 'AND':
            operation_result = children0[0] and children1[0]
            var_type = "bool"
        elif self.value.type == 'GT':
            operation_result = children0[0] > children1[0]
            var_type = "bool"
        elif self.value.type == 'LT':
            operation_result = children0[0] < children1[0]
            var_type = "bool"
        else:
            raise BufferError(f"Invalid operation of type {self.value.type}")
        return operation_result, var_type


class UnOp(Node):

    expr: Node

    def __init__(self, value: Token, expr: Node):
        super().__init__(value)
        self.expr = expr

    def evaluate(self, table):
        if self.value.type == 'UPLUS' or self.value.type == 'PLUS':
            return self.expr.evaluate(table)
        elif self.value.type == 'UMINUS' or self.value.type == 'MINUS':
            return -self.expr.evaluate(table)
        elif self.value.type == 'UNOT' or self.value.type == 'NOT':
            return not self.expr.evaluate(table)
        else:
            raise BufferError(f"Invalid operation of type {self.value.type}")


class IntVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return int(self.value.value), "int"


class FloatVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return float(self.value.value), "float"


class StringVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return self.value.value, "string"


class BoolVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return bool(self.value.value), "bool"


class IdentifierVal(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return table.getVariable(self.value.value)


class NoOp(Node):

    def __init__(self, value: Token):
        super().__init__(value)

    def evaluate(self, table: SymbolTable):
        return 0, "void"
