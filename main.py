
import os
from datetime import datetime
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
    try:
        # Formata em dicionario
        # CPF;Nome;Endereço;TelefoneFixo;TelefoneCelular;DataNascimento
        cpf, nome, endereco, tel_fixo, tel_cel, data_nasc = linha.split(';')

        return {
            'cpf': cpf,
            'nome': nome,
            'endereco': endereco,
            'tel_fixo': tel_fixo,
            'tel_cel': tel_cel,
            'data_nasc': datetime.strptime(data_nasc, '%Y-%m-%d').date()
        }
    except:
        print(f"Erro ao parsear cliente: {linha}")

def format_cliente(c):
    # Converte dicionário para string
    return f"{c['cpf']};{c['nome']};{c['endereco']};{c['tel_fixo']};{c['tel_cel']};{c['data_nasc'].isoformat()}"

def listar_clientes():
    try:
        linhas = ler_arquivo('clientes.txt')
        clientes = []
        for linha in linhas:
            cliente = parse_cliente(linha)
            clientes.append(cliente)
        
        if not clientes:
            print("Não há clientes cadastrados.")
        else:
            for c in clientes:
                print(c)

    except Exception as e:
        print(f"Erro ao listar clientes: {e}")

def buscar_cliente(cpf):
    return

def incluir_cliente():

    # Pegar as informações do cliente
    cpf = input("CPF: ").strip()
    if buscar_cliente(cpf):
        print("Cliente já existe com esse CPF.")
        return
    nome = input("Nome: ").strip()
    endereco = input("Endereço: ").strip()
    tel_fixo = input("Telefone fixo: ").strip()
    tel_cel = input("Telefone celular: ").strip()
    data_nasc = datetime.strptime(input("Data de nascimento (YYYY-MM-DD): "), '%Y-%m-%d').date()

    c = {
        'cpf': cpf, 'nome': nome, 'endereco': endereco,
        'tel_fixo': tel_fixo, 'tel_cel': tel_cel, 'data_nasc': data_nasc
    }

    # Verificar se o arquivo existe e gravar o cliente, ele será adicionado ao final do arquivo
    # A função ler arquivo já verifica se o arquivo existe e retorna uma lista vazia se não existir
    linhas = ler_arquivo('clientes.txt')
    linhas.append(format_cliente(c))
    gravar_arquivo('clientes.txt', linhas)
    print("Cliente incluído.")


def alterar_cliente():

    return

def excluir_cliente():
    return

def submenu_clientes():
  while True:
        print("\n" + "─"*40)
        print("         GERENCIAMENTO DE CLIENTES")
        print("─"*40)
        print("│  1 │ Listar Todos os Clientes")
        print("│  2 │ Buscar Cliente por CPF")
        print("│  3 │ Cadastrar Novo Cliente")
        print("│  4 │ Alterar Dados do Cliente")
        print("│  5 │ Excluir Cliente")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*40)
        
        opcao = input("Digite sua opção [0-5]: ").strip()
        
        if opcao == '1':
            listar_clientes()
            
        elif opcao == '2':
            cpf = input("\n📋 Digite o CPF do cliente: ").strip()
            if cpf:
                cliente = buscar_cliente(cpf)
                if cliente:
                    print(f"\n✅ Cliente encontrado:")
                    print(cliente)
                else:
                    print("\n❌ Cliente não encontrado.")
            else:
                print("\n⚠️  CPF não pode estar vazio.")
            input("\nPressione ENTER para continuar...")
            
        elif opcao == '3':
            incluir_cliente()
            
        elif opcao == '4':
            alterar_cliente()
            
        elif opcao == '5':
            excluir_cliente()
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")





'''MANTER FORMATAÇÂO DOS DADOS COMO NO EXEMPLO ABAIXO

f"{c['cpf']};{c['nome']};{c['endereco']};{c['tel_fixo']};{c['tel_cel']};{c['data_nasc'].isoformat()}"

com ; entre os campos e data no formato (AAAA-MM-DD)

pra n dar BO

'''
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
