from compiler.parser import DothParser
from compiler.lexical import DothLexer
from helpers.symbolTable import SymbolTable
from llvm.codegen import CodeGen
import sys

if __name__ == '__main__':
    code = None
    if len(sys.argv) > 1:
        f = sys.argv[1]
        with open(f, "r") as tmp:
            code = tmp.read()

    codegen = CodeGen()
    lexer = DothLexer()
    parser = DothParser(codegen.module, codegen.builder, codegen.printf)
    table = SymbolTable()
    if code:
        tokens = lexer.tokenize(code)
        nodes = parser.parse(tokens)
        nodes.evaluate(table)
        codegen.createIr()
        codegen.saveIr('./out/output.ll')
    else:
        while True:
            try:
                text = input('>>> ')
            except EOFError:
                break
            if text:
                tokens = lexer.tokenize(text)
                node = parser.parse(tokens)
                node.evaluate(table)
