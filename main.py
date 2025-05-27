

# Importa OS para manipulação de arquivos
import os
# Importa datetime para manipulação mais precisa de datas
from datetime import datetime


# =============== Helpers =========================

def ler_arquivo(nome_arquivo):
    # Verifica se o arquivo existe
    if not os.path.exists(nome_arquivo):
        return []
    
    try:
        #Tenta abrir o arquivo e ler as linhas, r de read
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
    # isoformat() converte a data para o formato YYYY-MM-DD

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
                print(f"CPF: {c['cpf']}, Nome: {c['nome']}, Endereço: {c['endereco']}, "
                      f"Telefone Fixo: {c['tel_fixo']}, Telefone Celular: {c['tel_cel']}, "
                      f"Data de Nascimento: {c['data_nasc'].isoformat()}")

    except Exception as e:
        print(f"Erro ao listar clientes: {e}")

def buscar_cliente(cpf):
    try:
        # Verifica se o arquivo existe e lê as linhas e procura o cliente pelo CPF
        for l in ler_arquivo('clientes.txt'):
            c = parse_cliente(l)
            if c['cpf'] == cpf:
                return c
        return  # Retorna se não encontrar o cliente, não precisa de mensagem
                # Usuário não precisa saber que aquele CPF não está cadastrado
    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
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
    try:
        cpf = input("Digite o CPF do cliente a ser alterado: ").strip()
        linhas = ler_arquivo('clientes.txt')
        nova_lista = []
        achou = False

        for l in linhas:

            # Não consegui reutilizar a função buscar_cliente, pois ela retorna o cliente e não a linha
            c = parse_cliente(l)
            if c['cpf'] == cpf:
                achou = True 
                print("Dados atuais do cliente: ")
                for key, value in c.items():
                    print(f"{key.capitalize()}: {value}")


                # Pegar as novas informações do cliente
                c['nome'] = input("Novo Nome: ").strip() or c['nome']
                c['endereco'] = input("Novo Endereço: ").strip() or c['endereco']
                c['tel_fixo'] = input("Novo Telefone fixo: ").strip() or c['tel_fixo']
                c['tel_cel'] = input("Novo Telefone celular: ").strip() or c['tel_cel']
                data_nasc_input = input("Nova Data de nascimento (YYYY-MM-DD): ").strip()
                if data_nasc_input:
                    c['data_nasc'] = datetime.strptime(data_nasc_input, '%Y-%m-%d').date()

                nova_lista.append(format_cliente(c))
            else:
                # Se não for o cliente a ser alterado, mantém a linha original
                nova_lista.append(l)

            
            if not achou:
                print("Cliente não encontrado.")
                return
            else:
                gravar_arquivo('clientes.txt', nova_lista)
                print("Cliente alterado.")
        
    except Exception as e:
        print(f"Erro ao alterar cliente: {e}")
        return

    

def excluir_cliente():
    # Mesma verificação de arquivo e leitura
    cpf = input("CPF do cliente a excluir: ").strip()
    linhas = ler_arquivo('clientes.txt')
    nova = []
    achou = False
    for l in linhas:
        c = parse_cliente(l)
        if c['cpf'] == cpf:
            achou = True

            print("Vai excluir:")
            for key, value in c.items():
                print(f"{key.capitalize()}: {value}")


            # Confirmação de exclusão
            confirmacao = input("Tem certeza que deseja excluir este cliente? (S/N): ").strip().upper()
            if confirmacao == 'S':
                print("Excluído.")
                continue
        # Se não for o cliente a ser excluído, mantém a linha original
        # Se for o cliente a ser excluído, não adiciona na nova lista
        nova.append(l)
    if not achou:
        print("Cliente não encontrado.")
    else:
        gravar_arquivo('clientes.txt', nova)


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
                    for key, value in cliente.items():
                        print(f"{key.capitalize()}: {value}")
                else:
                    print("\n❌ Cliente não encontrado.")
            else:
                print("\n⚠️  CPF não pode estar vazio.")

            #Input para continuar, mantendo a informação na tela como foco
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






# =============== Reservas =========================
def submenu_reservas():
    while True:
        print("\n" + "─"*40)
        print("         GERENCIAMENTO DE RESERVAS")
        print("─"*40)
        print("│  1 │ Listar Todas as Reservas")
        print("│  2 │ Buscar Reserva por Código")
        print("│  3 │ Cadastrar Nova Reserva")
        print("│  4 │ Alterar Dados da Reserva")
        print("│  5 │ Excluir Reserva")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*40)
        
        opcao = input("Digite sua opção [0-5]: ").strip()
        
        if opcao == '1':
            return
            
        elif opcao == '2':
            return
         
            
        elif opcao == '3':
            return
       
            
        elif opcao == '4':
            return
        
            
        elif opcao == '5':
            return
         
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")















# =============== Apartamentos =========================
def submenu_apartamentos():
    """Submenu para gerenciamento de apartamentos."""
    while True:
        print("\n" + "─"*40)
        print("        GERENCIAMENTO DE APARTAMENTOS")
        print("─"*40)
        print("│  1 │ Listar Todos os Apartamentos")
        print("│  2 │ Buscar Apartamento por Código")
        print("│  3 │ Cadastrar Novo Apartamento")
        print("│  4 │ Alterar Dados do Apartamento")
        print("│  5 │ Excluir Apartamento")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*40)
        
        opcao = input("Digite sua opção [0-5]: ").strip()
        
        if opcao == '1':
            return
         
            
        elif opcao == '2':
            return
       
           
            
        elif opcao == '3':
            return
    
            
        elif opcao == '4':
            return
        
            
        elif opcao == '5':
            return
       
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")















# =============== ReservaApart =========================
def submenu_reserva_apto():
    """Submenu para gerenciamento de vinculação reserva-apartamento."""
    while True:
        print("\n" + "─"*45)
        print("       VINCULAÇÃO RESERVA-APARTAMENTO")
        print("─"*45)
        print("│  1 │ Listar Todas as Vinculações")
        print("│  2 │ Buscar Vinculação Específica")
        print("│  3 │ Criar Nova Vinculação")
        print("│  4 │ Alterar Vinculação")
        print("│  5 │ Excluir Vinculação")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*45)
        
        opcao = input("Digite sua opção [0-5]: ").strip()
        
        if opcao == '1':
            return
          
            
        elif opcao == '2':
            return
           
            
        elif opcao == '3':
            return
           
            
        elif opcao == '4':
            return
           
            
        elif opcao == '5':
            return
           
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")













# =============== Relatórios =========================
def submenu_relatorios():
    """Submenu para relatórios e consultas do sistema."""
    while True:
        print("\n" + "─"*45)
        print("           RELATÓRIOS E CONSULTAS")
        print("─"*45)
        print("│  1 │ Reservas por Apartamento")
        print("│  2 │ Reservas por Cliente")
        print("│  3 │ Clientes por Período de Reserva")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*45)
        
        opcao = input("Digite sua opção [0-3]: ").strip()
        
        if opcao == '1':
            print("\n📊 Gerando relatório de reservas por apartamento...")
            return
      
            
        elif opcao == '2':
            print("\n📊 Gerando relatório de reservas por cliente...")
            return
    
            
        elif opcao == '3':
            print("\n📊 Gerando relatório de clientes por período...")
            return
          
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 3.")
            input("Pressione ENTER para continuar...")









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
