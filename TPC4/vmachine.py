import json
import ply.lex as lex
from datetime import date

STOCK_FILE = "stock.json"

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'ADICIONAR',
    'VALOR',
    'CODIGO'
)

t_LISTAR = r'LISTAR'
t_MOEDA = r'MOEDA'
t_SELECIONAR = r'SELECIONAR'
t_SAIR = r'SAIR'
t_ADICIONAR = r'ADICIONAR'
t_CODIGO = r'[A-D]\d{2}'
t_VALOR = r'((2e)|(1e)|(50c)|(20c)|(10c)|(5c)|(2c)|(1c))+'

t_ignore = " \t\n"

def t_error(t):
    print(f"maq: Token inválido -> '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def carregar_stock():
    try:
        with open(STOCK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_stock(stock):
    with open(STOCK_FILE, 'w', encoding='utf-8') as f:
        json.dump(stock, f, ensure_ascii=False, indent=4)

def listar_produtos(stock):
    print("maq:")
    print(f"{'Cod':<6} | {'Nome':<20} | {'Quant':<6} | {'Preço'}")
    print("-"*50)
    for p in stock:
        print(f"{p['cod']:<6} | {p['nome']:<20} | {p['quant']:<6} | {p['preco']}€")

def procurar_produto(stock, codigo):
    return next((p for p in stock if p['cod'].upper() == codigo.upper()), None)

def adicionar_produto(stock, cod, nome, quant, preco):
    p = procurar_produto(stock, cod)
    if p:
        p['quant'] += quant
    else:
        stock.append({"cod": cod, "nome": nome, "quant": quant, "preco": preco})

def dispensar_produto(produto, saldo):
    if produto['quant'] == 0:
        print("maq: Produto esgotado.")
        return saldo, False
    if saldo < produto['preco']:
        falta = produto['preco'] - saldo
        print(f"maq: Saldo insuficiente. Falta {falta:.2f}€.")
        return saldo, False
    produto['quant'] -= 1
    saldo -= produto['preco']
    print(f'maq: Pode retirar o produto "{produto["nome"]}".')
    return round(saldo,2), True

def processar_moedas(lista_moedas, saldo):
    for m in lista_moedas:
        if m.endswith('e'):
            saldo += float(m[:-1])
        elif m.endswith('c'):
            saldo += float(m[:-1])/100
    return round(saldo,2)

def calcular_troco(saldo):
    moedas = [2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    troco = []
    for m in moedas:
        qtd = int(saldo // m)
        if qtd:
            troco.append((qtd, m))
            saldo = round(saldo - qtd*m,2)
    return troco

class Maquina:
    def __init__(self):
        self.stock = carregar_stock()
        self.saldo = 0.0
        self.comandos = {
            'LISTAR': self.cmd_listar,
            'MOEDA': self.cmd_moeda,
            'SELECIONAR': self.cmd_selecionar,
            'SAIR': self.cmd_sair,
            'ADICIONAR': self.cmd_adicionar
        }

    def cmd_listar(self, tokens):
        listar_produtos(self.stock)

    def cmd_moeda(self, tokens):
        valores = [t.value for t in tokens if t.type=='VALOR']
        self.saldo = processar_moedas(valores, self.saldo)
        print(f"maq: Saldo = {int(self.saldo)}e{int((self.saldo%1)*100)}c")

    def cmd_selecionar(self, tokens):
        codigos = [t.value for t in tokens if t.type=='CODIGO']
        if not codigos:
            print("maq: Código não fornecido.")
            return
        produto = procurar_produto(self.stock, codigos[0])
        if not produto:
            print("maq: Produto inexistente.")
            return
        self.saldo, sucesso = dispensar_produto(produto, self.saldo)

    def cmd_adicionar(self, tokens):
        if len(tokens)<5:
            print("Uso: ADICIONAR <cod> <nome> <quant> <preço>")
            return
        _, cod, nome, quant, preco = [t.value for t in tokens[:5]]
        adicionar_produto(self.stock, cod, nome, int(quant), float(preco))
        print(f"maq: Produto {cod} adicionado/atualizado.")

    def cmd_sair(self, tokens):
        troco = calcular_troco(self.saldo)
        if troco:
            s = ", ".join([f"{q}x {int(m*100)}c" if m<1 else f"{q}x {int(m)}e" for q,m in troco])
            print(f"maq: Pode retirar o troco: {s}.")
        print("maq: Até à próxima!")
        guardar_stock(self.stock)
        exit(0)

    def interpretar(self, linha):
        lexer.input(linha)
        tokens_lidos = list(lexer)
        if not tokens_lidos:
            print("maq: Comando inválido.")
            return
        tipo = tokens_lidos[0].type
        func = self.comandos.get(tipo)
        if func:
            func(tokens_lidos)
        else:
            print("maq: Comando não reconhecido.")

def main():
    m = Maquina()
    print(f"maq: {date.today()}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    while True:
        linha = input(">> ").strip()
        m.interpretar(linha)

if __name__=="__main__":
    main()
