
import os
# =============== Helpers =========================

def ler_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = []
            for linha in arquivo:
                linha_limpa = linha.strip()
                if linha_limpa:
                    linhas.append(linha_limpa)
            return linhas
    except:
        print(f"Erro ao ler o arquivo: {nome_arquivo}")
        return []


def gravar_arquivo(nome_arquivo, linhas):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            if linhas:
                arquivo.write('\n'.join(linhas) + '\n')
        return True
    except:
        print(f"Erro ao gravar o arquivo: {nome_arquivo}")
        return False


# =============== Clientes =========================

def parse_cliente(linha):
    # Formata em dicionario
    return

def format_cliente(c):
    # Converte dicionário para string
    return f"{c['cpf']};{c['nome']};{c['endereco']};{c['tel_fixo']};{c['tel_cel']};{c['data_nasc'].isoformat()}"

def listar_clientes():
    return

def buscar_cliente(cpf):
    return

def incluir_cliente():
    return

def alterar_cliente():

    return

def excluir_cliente():
    return

def submenu_clientes():
    while True:
        print("\n-- Submenu Clientes --")
        print("1 Listar todos")
        print("2 Listar um")
        print("3 Incluir")
        print("4 Alterar")
        print("5 Excluir")
        print("0 Voltar")
        op = input("Escolha: ")
        if op == '1': listar_clientes()
        elif op == '2':
            cpf = input("CPF: ").strip()
            c = buscar_cliente(cpf)
            print(c or "Não encontrado.")
        elif op == '3': incluir_cliente()
        elif op == '4': alterar_cliente()
        elif op == '5': excluir_cliente()
        elif op == '0': break
        else: print("Opção inválida.")

# =============== Reservas =========================


def submenu_reservas():
    return
# =============== Apartamentos =========================

def submenu_apartamentos():
    return
# =============== ReservaApart =========================

def submenu_reserva_apto():
    return
# =============== Relatórios =========================


def submenu_relatorios():
    return

# =============== Menu Principal =========================
def main():
    while True:
        print("\n" + "="*50)
        print("           SISTEMA DE GERENCIAMENTO HOTELEIRO")
        print("="*50)
        print("│  1 │ Gerenciar Clientes")
        print("│  2 │ Gerenciar Reservas")
        print("│  3 │ Gerenciar Apartamentos")
        print("│  4 │ Vincular Reserva-Apartamento")
        print("│  5 │ Relatórios e Consultas")
        print("│  6 │ Sair do Sistema")
        print("="*50)
        
        opcao = input("Digite sua opção [1-6]: ").strip()
        
        if opcao == '1':
            submenu_clientes()
        elif opcao == '2':
            submenu_reservas()
        elif opcao == '3':
            submenu_apartamentos()
        elif opcao == '4':
            submenu_reserva_apto()
        elif opcao == '5':
            submenu_relatorios()
        elif opcao == '6':
            print("\n" + "="*50)
            print("    Obrigado por usar nosso sistema!")
            print("           Até logo! 👋")
            print("="*50)
            break
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 1 e 6.")
            input("Pressione ENTER para continuar...")


main()
