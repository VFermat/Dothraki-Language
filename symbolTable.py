from typing import NoReturn, Dict, Union
from sly.lex import Token


class SymbolTable:

    table: Dict[str, Token]

    def __init__(self):
        self.table = {}

    def getVariable(self, variable: str) -> Token:
        if variable in self.table:
            return self.table[variable]["value"], self.table[variable]["varType"]
        raise KeyError(f"No variable named {variable}")

    def declareVariable(
        self, variable: str, value: Union[int, str, bool], varType: str
    ) -> NoReturn:
        if variable in self.table:
            raise NameError(f"Variable {variable} already declared")
        self.table[variable] = {"value": value, "varType": varType}

    def setVariable(
        self, variable: str, value: Union[int, str, bool], varType: str
    ) -> NoReturn:
        if variable not in self.table:
            raise NameError(f"Variable {variable} not declared")
        elif varType != self.table[variable]["varType"]:
            if varType in ['int', 'float'] and self.table[variable]["varType"] == 'bool':
                value = bool(value)
            elif varType in ['bool', 'float'] and self.table[variable]["varType"] == 'int':
                value = int(value)
            elif varType in ['int', 'bool'] and self.table[variable]["varType"] == 'float':
                value = float(value)
            else:
                raise TypeError()
        self.table[variable]["value"] = value
