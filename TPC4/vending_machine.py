import ply.lex as lex
import json
from datetime import date

tokens = [
    "LISTAR",
    "SELECIONAR",
    "SAIR",
    "MOEDA",
    "CODIGO",
    "VALOR"
]

t_LISTAR = r'LISTAR'
t_SELECIONAR = r'SELECIONAR'
t_SAIR = r'SAIR'
t_MOEDA = r'MOEDA' 
t_CODIGO = r'[A-Z]\d\d'
t_VALOR = r'((2e)|(1e)|(50c)|(20c)|(10c)|(5c)|(2c)|(1c))+'  

t_ignore = " \t\n"

def t_error(t):
    print(f"maq: Token inválido -> '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def listar(stock):
    print("maq:")
    print(f"{'cod':<6} | {'nome':<20} | {'quant':<8} | {'preço'}")
    print("-" * 50)
    for item in stock:
        print(f"{item['cod']:<6} | {item['nome']:<20} | {item['quant']:<8} | {item['preco']}€")


def adicionar_saldo(saldo, moedas):
    for moeda in moedas:
        if moeda.endswith("e"):
            saldo += float(moeda[:-1])
        else:
            saldo += float(moeda[:-1]) * 0.01
    print(f"maq: Saldo = {int(saldo)}e{int((saldo % 1) * 100)}c")
    return saldo

def pedido(saldo, stock, codigo):
    produto = next((s for s in stock if s["cod"] == codigo), None)

    if produto is None:
        print("maq: Código inválido.")
    elif produto["quant"] == 0:
        print("maq: Produto esgotado.")
    elif produto["preco"] > saldo:
        print(f"maq: Saldo insuficiente.\nSaldo: {saldo:.2f}; Pedido: {produto['preco']:.2f}")
    else:
        produto["quant"] -= 1
        saldo = saldo - produto["preco"]
        print(f'maq: Pode retirar o produto "{produto["nome"]}".')
        print(f"maq: Saldo = {int(saldo)}e{int((saldo % 1) * 100)}c")

    return saldo

    

def dar_troco(saldo,troco = None):
    if troco is None:
        troco = []
    if 2 <= saldo:
        troco.append("2e")
        return(dar_troco(saldo-2,troco))
    elif 1 <= saldo:
        troco.append("1e")
        return(dar_troco(saldo-1,troco))
    elif 0.50 <= saldo:
        troco.append("50c")
        return(dar_troco(saldo-0.5,troco))
    elif 0.2 <= saldo:
        troco.append("20c")
        return(dar_troco(saldo-0.2,troco))
    elif 0.1 <= saldo:
        troco.append("10c")
        return(dar_troco(saldo-0.1,troco))
    elif 0.05 <= saldo:
        troco.append("5c")
        return(dar_troco(saldo-0.05,troco))
    elif 0.02 < saldo:
        troco.append("2c")
        return(dar_troco(saldo-0.02,troco))
    elif 0.01 <= saldo:
        troco.append("1c")
        return(dar_troco(saldo-0.01,troco))
    else:
        return troco


def ler_input(stock,linha,saldo):
    lexer.input(linha)
    tokens_lidos = list(lexer)

    if not tokens_lidos:
        print("maq: Comando inválido.")
        return saldo

    comando = tokens_lidos[0].value

    if comando == "LISTAR":
        listar(stock)
    
    elif comando == "MOEDA":
        moedas = [l.value for l in tokens_lidos[1:] if l.type == "VALOR"]
        saldo = adicionar_saldo(saldo,moedas)

    elif comando == "SELECIONAR":
        if tokens_lidos[1].type == "CODIGO":
            saldo = pedido(saldo,stock,tokens_lidos[1].value)

    elif comando == "SAIR":
        troco = dar_troco(saldo)
        print("maq: Pode retirar o troco:", ", ".join(troco))
        print("maq: Até à próxima!")
        exit(0)
    return saldo


def vending_machine():
    file = open("stock.json","r",encoding="utf-8")
    stock = json.load(file)
    saldo = 0
    print(f"maq: {date.today()}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    while True:
        linha = input(">> ").strip()
        saldo = ler_input(stock,linha,saldo)

if __name__ == "__main__":
    vending_machine()