from parser import DothParser
from lexical import DothLexer
import sys

if __name__ == '__main__':
    code = None
    if len(sys.argv) > 1:
        f = sys.argv[1]
        with open(f, "r") as tmp:
            code = tmp.read()
    lexer = DothLexer()
    parser = DothParser()
    if code:
        tokens = lexer.tokenize(code)
        parser.parse(tokens)
    else:
        while True:
            try:
                text = input('>>> ')
            except EOFError:
                break
            if text:
                tokens = lexer.tokenize(text)
                parser.parse(tokens)
