from compiler.parser import DothParser
from compiler.lexical import DothLexer
from helpers.symbolTable import SymbolTable
from llvm.codegen import CodeGen
import sys

if __name__ == '__main__':
    code = None
    if len(sys.argv) > 1:
        f = sys.argv[1]
        extension = f.split('.')[-1]
        if extension != 'dt':
            raise TypeError("Invalid file type for compiler.")
        with open(f, "r") as tmp:
            code = tmp.read()

    codegen = CodeGen()
    lexer = DothLexer()
    parser = DothParser(codegen.module, codegen.builder, codegen.printf)
    table = SymbolTable()
    tokens = lexer.tokenize(code)
    nodes = parser.parse(tokens)
    nodes.evaluate(table)
    codegen.createIr()
    codegen.saveIr('./out/output.ll')
