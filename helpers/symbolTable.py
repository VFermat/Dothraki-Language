from typing import NoReturn, Dict, Union
from sly.lex import Token


class SymbolTable:

    table: Dict[str, Token]

    def __init__(self):
        self.table = {}

    def getVariable(self, variable: str) -> Token:
        if variable in self.table:
            return self.table[variable]["pointer"], self.table[variable]["type"]
        raise KeyError(f"No variable named {variable}")

    def declareVariable(
        self, variable: str, ptr, var_type: str = "null"
    ) -> NoReturn:
        if variable in self.table:
            raise NameError(f"Variable {variable} already declared")
        self.table[variable] = {"pointer": ptr, "type": var_type}

    def setVariable(
        self, variable: str, ptr
    ) -> NoReturn:
        if variable not in self.table:
            raise NameError(f"Variable {variable} not declared")
        self.table[variable]["pointer"] = ptr
