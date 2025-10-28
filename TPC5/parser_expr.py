import ply.lex as lex

tokens = (
    'NUM',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t\n'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

current_token = None
token_stream = []
position = 0

def syntax_error(tok):
    print(f"Erro: símbolo inesperado '{tok.value}' ({tok.type})")
    exit(1)

def accept(expected):
    global current_token, position
    if current_token.type == expected:
        print(f"Consumido: {current_token.type} ({current_token.value})")
        position += 1
        current_token = token_stream[position]
    else:
        syntax_error(current_token)

def parse_expr():
    print("Reconhecido: Expr → Term Rest")
    parse_term()
    parse_rest()

def parse_rest():
    global current_token
    if current_token.type in ('PLUS', 'MINUS', 'TIMES', 'DIVIDE'):
        parse_op()
        parse_term()
        parse_rest()
        print("Reconhecido: Rest → Op Term Rest")
    elif current_token.type in ('RPAREN', 'EOF'):
        print("Reconhecido: Rest → ε")
    else:
        syntax_error(current_token)

def parse_term():
    global current_token
    if current_token.type == 'NUM':
        accept('NUM')
        print("Reconhecido: Term → NUM")
    elif current_token.type == 'LPAREN':
        accept('LPAREN')
        parse_expr()
        accept('RPAREN')
        print("Reconhecido: Term → ( Expr )")
    else:
        syntax_error(current_token)

def parse_op():
    global current_token
    ops = {'PLUS': '+', 'MINUS': '-', 'TIMES': '*', 'DIVIDE': '/'}
    op = current_token.type
    accept(op)
    print(f"Reconhecido: Op → '{ops[op]}'")

def run_parser(expression):
    global current_token, token_stream, position
    lexer.input(expression)
    token_stream = list(lexer)
    eof = lex.LexToken()
    eof.type = 'EOF'
    eof.value = ''
    token_stream.append(eof)
    position = 0
    current_token = token_stream[position]
    print(f"\nExpressão: {expression}")
    parse_expr()
    if current_token.type == 'EOF':
        print("Expressão reconhecida completamente!")
    else:
        syntax_error(current_token)

if __name__ == "__main__":
    exemplos = [
        "3 + 4",
        "(2 + 5) * (8 - 3)",
        "10 / (2 + 3)"
    ]
    for e in exemplos:
        run_parser(e)
