

# Importa OS para manipulação de arquivos
import os
# Importa datetime para manipulação mais precisa de datas
from datetime import datetime, date


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

def listar_clientes(clientes):
    try:
        if not clientes:
            print("Não há clientes cadastrados.")
        else:
            for c in clientes:
                print(f"CPF: {c['cpf']}, Nome: {c['nome']}, Endereço: {c['endereco']}, "
                      f"Telefone Fixo: {c['tel_fixo']}, Telefone Celular: {c['tel_cel']}, "
                      f"Data de Nascimento: {c['data_nasc'].isoformat()}")

    except Exception as e:
        print(f"Erro ao listar clientes: {e}")

def buscar_cliente(cpf, clientes):
    for c in clientes:
        if c['cpf'] == cpf:
            return c
    return None


def obter_idade_valida(data_nasc):
    hoje = date.today()
    idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
    while idade <= 0 or idade >= 130:
        print(f"Idade inválida ({idade} anos). A idade deve estar entre 1 e 129 anos.")
        try:
            data_str = input("Digite novamente a data de nascimento (YYYY-MM-DD): ").strip()
            data_nasc = datetime.strptime(data_str, '%Y-%m-%d').date()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        except ValueError:
            print("Formato de data inválido.")
            continue
    return data_nasc

def incluir_cliente(clientes):
    # Pegar as informações do cliente
    cpf = input("CPF: ").strip()
    if buscar_cliente(cpf, clientes):
        print("Cliente já existe com esse CPF.")
        return
    nome = input("Nome: ").strip()
    endereco = input("Endereço: ").strip()
    tel_fixo = input("Telefone fixo: ").strip()
    tel_cel = input("Telefone celular: ").strip()
    while True:
        try:
            data_nasc = datetime.strptime(input("Data de nascimento (YYYY-MM-DD): "), '%Y-%m-%d').date()
            data_nasc = obter_idade_valida(data_nasc)
            break
        except ValueError:
            print("Formato de data inválido. Tente novamente.")

    clientes.append({
        'cpf': cpf,
        'nome': nome,
        'endereco': endereco,
        'tel_fixo': tel_fixo,
        'tel_cel': tel_cel,
        'data_nasc': data_nasc
    })
    print("Cliente incluído.")


def alterar_cliente(clientes):
    try:
        cpf = input("Digite o CPF do cliente a ser alterado: ").strip()
        cliente = buscar_cliente(cpf, clientes)
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        print("\nDados atuais do cliente:")
        for k, v in cliente.items():
            print(f"{k.capitalize()}: {v}")

        nome = input("Novo Nome (ENTER para manter): ").strip() or cliente['nome']
        endereco = input("Novo Endereço (ENTER para manter): ").strip() or cliente['endereco']
        tel_fixo = input("Novo Telefone fixo (ENTER para manter): ").strip() or cliente['tel_fixo']
        tel_cel = input("Novo Telefone celular (ENTER para manter): ").strip() or cliente['tel_cel']
        data_str = input("Nova Data de nascimento (YYYY-MM-DD, ENTER para manter): ").strip()
        if data_str:
            try:
                nova_data = datetime.strptime(data_str, '%Y-%m-%d').date()
                nova_data = obter_idade_valida(nova_data)
                cliente['data_nasc'] = nova_data
            except ValueError:
                print("Formato de data inválido. Alteração cancelada.")
                return

        cliente.update({
            'nome': nome,
            'endereco': endereco,
            'tel_fixo': tel_fixo,
            'tel_cel': tel_cel
        })

        print("Cliente alterado")
    except Exception as e:
        print(f"Erro ao alterar cliente: {e}")
        return

    

def excluir_cliente(clientes):
    cpf = input("CPF do cliente a excluir: ").strip()
    cliente = buscar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado.")
        return
    print("Vai excluir:")
    for k, v in cliente.items():
        print(f"{k.capitalize()}: {v}")
    confirm = input("Tem certeza que deseja excluir este cliente? (S/N): ").strip().upper()
    if confirm == 'S':
        clientes.remove(cliente)
        print("Cliente excluído")
    else:
        print("Exclusão cancelada.")


def submenu_clientes():
  cliente_arquivo = 'clientes.txt'
  linhas = ler_arquivo(cliente_arquivo)
  clientes = [] # Lista para armazenar os clientes (um dic para cada cliente)
  for l in linhas:
        cliente = parse_cliente(l)
        if cliente is not None:
            clientes.append(cliente)

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
            listar_clientes(clientes)
            
        elif opcao == '2':
            cpf = input("\n📋 Digite o CPF do cliente: ").strip()
            if cpf:
                cliente = buscar_cliente(cpf, clientes)
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
            incluir_cliente(clientes)
            
        elif opcao == '4':
            alterar_cliente(clientes)
            
        elif opcao == '5':
            excluir_cliente(clientes)
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")
    
  novas_linhas = []
  for c in clientes:
        linha_formatada = format_cliente(c)
        novas_linhas.append(linha_formatada)
  if gravar_arquivo(cliente_arquivo, novas_linhas):
        print("Alterações salvas em arquivo.")
  else:
        print("Falha ao salvar alterações.")



# =============== Reservas =========================

def parse_reserva(linha):
    codigo, cpf = linha.split(';')
    return {'codigo': codigo, 'cpf': cpf}

def format_reserva(r):
    return f"{r['codigo']};{r['cpf']}"


def listar_reservas(reservas):
    if not reservas:
        print("Sem reservas.")
    
    for r in reservas:
        print(f"Código: {r['codigo']}, CPF do Cliente: {r['cpf']}")

def buscar_reserva(codigo, reservas):
    for r in reservas:
        if r['codigo'] == codigo:
            return r
    return None

def incluir_reserva(reservas, clientes):
    codigo = input("Código da reserva: ").strip()
    if buscar_reserva(codigo, reservas):
        print("Já existe uma reserva com esse código.")
        return
    cpf = input("CPF do cliente: ").strip()
    if not buscar_cliente(cpf, clientes):
        print("Cliente não encontrado.")
        return
    
    reservas.append({'codigo': codigo, 'cpf': cpf})
    print("Reserva incluída.")


def alterar_reserva(reservas, clientes):
    codigo = input("Código da reserva a alterar: ").strip()
    r = buscar_reserva(codigo, reservas)
    if not r:
        print("Reserva não encontrada.")
        return
    print("Dados atuais da reserva:")
    print(f"Código: {r['codigo']}, CPF: {r['cpf']}")
    novo_cpf = input("Novo CPF do cliente (ENTER para manter): ").strip() or r['cpf']
    if not any(c['cpf'] == novo_cpf for c in clientes):
        print("Cliente não encontrado.")
        return
    r['cpf'] = novo_cpf
    print("Reserva alterada.")

def excluir_reserva(reservas):
    codigo = input("Código da reserva a excluir: ").strip()
    r = buscar_reserva(codigo, reservas)
    if not r:
        print("Reserva não encontrada.")
        return
    print("Excluindo reserva:")
    print(f"Código: {r['codigo']}, CPF: {r['cpf']}")
    if input("Confirmar exclusão (S/N): ").strip().upper() == 'S':
        reservas.remove(r)
        print("Reserva excluída em memória.")
    else:
        print("Cancelado.")

def submenu_reservas():
    reserva_arquivo = 'reservas.txt'
    linhas = ler_arquivo(reserva_arquivo)
    reservas = []  # Lista para armazenar as reservas (um dic para cada reserva
    for l in linhas:
        reserva = parse_reserva(l)
        if reserva is not None:
            reservas.append(reserva)
    
    cliente_arquivo = 'clientes.txt'
    linhas = ler_arquivo(cliente_arquivo)
    clientes = [] # Lista para armazenar os clientes (um dic para cada cliente)
    for l in linhas:
        cliente = parse_cliente(l)
        if cliente is not None:
            clientes.append(cliente)

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
            listar_reservas(reservas)
        elif opcao == '2':
            codigo = input("\n📋 Digite o código da reserva: ").strip()
            if codigo:
                reserva = buscar_reserva(codigo, reservas)
                if reserva:
                    print(f"\n✅ Reserva encontrada:")
                    for key, value in reserva.items():
                        print(f"{key.capitalize()}: {value}")
                else:
                    print("\n❌ Reserva não encontrada.")
            else:
                print("\n⚠️  Código não pode estar vazio.")

            #Input para continuar, mantendo a informação na tela como foco
            input("\nPressione ENTER para continuar...")
            
        elif opcao == '3':
            incluir_reserva(reservas, clientes)     
        elif opcao == '4':
            alterar_reserva(reservas, clientes)    
        elif opcao == '5':
            excluir_reserva(reservas)     
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break     
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")
    
    novas_linhas = []
    for r in reservas:
        linha_formatada = format_reserva(r)
        novas_linhas.append(linha_formatada)
    if gravar_arquivo(reserva_arquivo, novas_linhas):
        print("Alterações salvas em arquivo.")
    else:
        print("Falha ao salvar alterações.")




# =============== Apartamentos =========================

def parse_apartamento(linha):
    try:
        codigo, descricao, adulto, crianca, valor = linha.split(';')
        return {
            'codigo': codigo,
            'descricao': descricao,
            'adultos': int(adulto),
            'criancas': int(crianca),
            'valor': float(valor)
        }
    except:
        print(f"Erro ao parsear apartamento: {linha}")

def format_apartamento(a):
    return f"{a['codigo']};{a['descricao']};{a['adultos']};{a['criancas']};{a['valor']}"

def listar_apartamentos(apartamentos):
    if not apartamentos:
        print("Sem apartamentos.")
    else:
        for a in apartamentos:
            print(f"Código: {a['codigo']}, Descrição: {a['descricao']}, Adultos: {a['adultos']}, Crianças: {a['criancas']}, Valor: {a['valor']}")

def buscar_apartamento(codigo, apartamentos):
    for a in apartamentos:
        if a['codigo'] == codigo:
            return a
    return None

def incluir_apartamento(apartamentos):
    codigo = input("Código do apartamento: ").strip()
    if buscar_apartamento(codigo, apartamentos):
        print("❌ Já existe um apartamento com este código.")
        return
    descricao = input("Descrição: ").strip()

    while True:
        try:
            adulto = int(input("Adultos: ").strip())
            if adulto < 0:
                print("❌ O número de adultos não pode ser negativo.")
                continue
            break
        except:
            print("❌ Entrada inválida. Digite um número inteiro.")

    while True:
        try:
            crianca = int(input("Crianças: ").strip())
            if crianca < 0:
                print("❌ O número de crianças não pode ser negativo.")
                continue
            break
        except:
            print("❌ Entrada inválida. Digite um número inteiro.")

    while True:
        try:
            valor = float(input("Valor: ").strip())
            if valor < 0:
                print("❌ O valor não pode ser negativo.")
                continue
            break
        except:
            print("❌ Entrada inválida. Digite um número decimal.")

    a = {'codigo': codigo, 'descricao': descricao, 'adultos': adulto, 'criancas': crianca, 'valor': valor}
    apartamentos.append(a)
    print("✅ Apartamento incluído com sucesso.")

def alterar_apartamento(apartamentos):
    codigo = input("Código a alterar: ").strip()
    achou = False
    for a in apartamentos:
        if a['codigo'] == codigo:
            achou = True
            print("Atual:", a)
            nova_descricao = input("Nova descrição (deixe vazio para manter): ").strip()
            if nova_descricao:
                a['descricao'] = nova_descricao

            novo_adultos = input("Novos adultos (deixe vazio para manter): ").strip()
            if novo_adultos:
                while True:
                    try:
                        valor = int(novo_adultos)
                        if valor < 0:
                            print("❌ O número de adultos não pode ser negativo.")
                            novo_adultos = input("Novos adultos (deixe vazio para manter): ").strip()
                        else:
                            a['adultos'] = valor
                            break
                    except:
                        print("❌ Entrada inválida. Digite um número inteiro.")
                        novo_adultos = input("Novos adultos (deixe vazio para manter): ").strip()

            novo_criancas = input("Novas crianças (deixe vazio para manter): ").strip()
            if novo_criancas:
                while True:
                    try:
                        valor = int(novo_criancas)
                        if valor < 0:
                            print("❌ O número de crianças não pode ser negativo.")
                            novo_criancas = input("Novas crianças (deixe vazio para manter): ").strip()
                        else:
                            a['criancas'] = valor
                            break
                    except:
                        print("❌ Entrada inválida. Digite um número inteiro.")
                        novo_criancas = input("Novas crianças (deixe vazio para manter): ").strip()

            nv = input("Novo valor (deixe vazio para manter): ").strip()
            if nv:
                while True:
                    try:
                        valor = float(nv)
                        if valor < 0:
                            print("❌ O valor não pode ser negativo.")
                            nv = input("Novo valor (deixe vazio para manter): ").strip()
                        else:
                            a['valor'] = valor
                            break
                    except:
                        print("❌ Entrada inválida. Digite um número decimal.")
                        nv = input("Novo valor (deixe vazio para manter): ").strip()

            print("✅ Apartamento alterado com sucesso.")
            break
    if not achou:
        print("❌ Apartamento não encontrado.")

def excluir_apartamento(apartamentos):
    codigo = input("Código a excluir: ").strip()
    achou = False
    for a in apartamentos[:]:  # usando cópia da lista para evitar problemas no laço
        if a['codigo'] == codigo:
            achou = True
            print("Excluindo:", a)
            if input("Confirmar? (S/N): ").strip().upper() == 'S':
                apartamentos.remove(a)
                print("✅ Apartamento excluído com sucesso.")
            else:
                print("❌ Exclusão cancelada.")
            break
    if not achou:
        print("❌ Apartamento não encontrado.")


def submenu_apartamentos():
    linhas = ler_arquivo('apartamentos.txt')
    apartamentos = []
    for linha in linhas:
        apartamento = parse_apartamento(linha)
        if apartamento:
            apartamentos.append(apartamento)

    while True:
        print("\n" + "─"*40)
        print("        GERENCIAMENTO DE APARTAMENTOS")
        print("─"*40)
        print("│  1 │ Listar Todos os Apartamentos")
        print("│  2 │ Buscar Apartamento por Código")
        print("│  3 │ Cadastrar Novo Apartamento")
        print("│  4 │ Alterar Dados do Apartamento")
        print("│  5 │ Excluir Apartamento")
        print("│  0 │ Voltar ao Menu Principal e Salvar Alterações")
        print("─"*40)
        
        opcao = input("Digite sua opção [0-5]: ").strip()
        
        if opcao == '1':
            listar_apartamentos(apartamentos)

        elif opcao == '2':
            codigo = input("\n📋 Digite o código do apartamento: ").strip()
            if codigo:
                apartamento = buscar_apartamento(codigo, apartamentos)
                if apartamento:
                    print(f"\n✅ Apartamento encontrado:")
                    for key, value in apartamento.items():
                        print(f"{key.capitalize()}: {value}")
                else:
                    print("\n❌ Apartamento não encontrado.")
            else:
                print("\n⚠️  Código não pode estar vazio.")
            input("\nPressione ENTER para continuar...")

        elif opcao == '3':
            incluir_apartamento(apartamentos)

        elif opcao == '4':
            alterar_apartamento(apartamentos)

        elif opcao == '5':
            excluir_apartamento(apartamentos)

        elif opcao == '0':
            linhas_formatadas = []
            for ap in apartamentos:
                linha_formatada = format_apartamento(ap)
                linhas_formatadas.append(linha_formatada)

            gravar_arquivo('apartamentos.txt', linhas_formatadas)
            print("\n💾 Alterações salvas com sucesso!")
            print("🔙 Voltando ao menu principal...")
            break

        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")


















# =============== ReservaApart =========================
def verifica_conflito_reserva(cod_apa, nova_entrada, nova_saida, cod_res=None): # Deixeando cod_res como opcional para ignorar 
                                                                                # a reserva atual ao alterar
    """
    Verifica se há conflito entre uma nova reserva e as reservas existentes.
    cod_apa: código do apartamento da nova reserva
    nova_entrada, nova_saida: datas da nova reserva
    cod_res: código da reserva (para ignorar ao alterar)
    """
    reservas_apto = ler_arquivo('reserva_apartamentos.txt')
    for linha in reservas_apto:
        ra = parse_reserva_apto(linha)
        if ra['cod_apa'] == cod_apa:
            # Ignora a reserva atual se for alteração
            if cod_res and ra['cod_res'] == cod_res: # se for alteração, ignora a reserva atual
                continue
            # Verifica sobreposição de períodos
            if (nova_saida >= ra['data_entrada'] and nova_entrada <= ra['data_saida']):
                print(f"❌ Conflito com reserva existente: Apartamento {ra['cod_res']} já tem reserva para o período de {ra['data_entrada']} a {ra['data_saida']}")
                return True
    return False


def parse_reserva_apto(linha):
    try:
        cod_res, cod_apa, data_entrada, data_saida = linha.split(';')
        return {
            'cod_res': cod_res,
            'cod_apa': cod_apa,
            'data_entrada': datetime.strptime(data_entrada, '%Y-%m-%d').date(),
            'data_saida': datetime.strptime(data_saida, '%Y-%m-%d').date()
        }
    except:
        print(f"Erro ao parsear vinculação: {linha}")

def format_reserva_apto(r):
    return f"{r['cod_res']};{r['cod_apa']};{r['data_entrada'].isoformat()};{r['data_saida'].isoformat()}"

def listar_reservas_apto():
    reserva_aptos = []
    reservas_apto = ler_arquivo('reserva_apartamentos.txt')
    for linha in reservas_apto:
        reserva_apto = parse_reserva_apto(linha)
        reserva_aptos.append(reserva_apto)
    if not reserva_aptos:
        print("Sem reservas de apartamento.")
    else:
        for ra in reserva_aptos:
            print(f"Reserva: {ra['cod_res']}, Apartamento: {ra['cod_apa']}, Entrada: {ra['data_entrada'].strftime('%d/%m/%Y %H:%M:%S')}, Saída: {ra['data_saida'].strftime('%d/%m/%Y %H:%M:%S')}")

def buscar_reserva_apto(cod_res, cod_apa):
    reservas_apto = ler_arquivo('reserva_apartamentos.txt')
    for linha in reservas_apto:
        ra = parse_reserva_apto(linha)
        if ra['cod_res']==cod_res and ra['cod_apa']==cod_apa:
            return ra
    return None

def incluir_reserva_apto():
    cod_res = input("Código da reserva: ").strip()
    cod_apa = input("Código do apartamento: ").strip()
    
    if buscar_reserva_apto(cod_res, cod_apa):
        print("❌ Já existe uma reserva com esse código e apartamento.")
        return

    data_entrada = datetime.strptime(input("Entrada (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()
    data_saida = datetime.strptime(input("Saída (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()

    # Verifica se entrada é antes da saída
    if data_entrada >= data_saida:
        print("❌ Data de entrada deve ser anterior à data de saída.")
        return

    # Verifica conflitos
    if verifica_conflito_reserva(cod_apa, data_entrada, data_saida):
        print("❌ Não é possível realizar a reserva devido a conflito de datas.")
        return

    ra = {'cod_res': cod_res, 'cod_apa': cod_apa, 'data_entrada': data_entrada, 'data_saida': data_saida}
    linhas = ler_arquivo('reserva_apartamentos.txt')
    linhas.append(format_reserva_apto(ra))
    gravar_arquivo('reserva_apartamentos.txt', linhas)
    print("✅ Reserva de apartamento incluída com sucesso.")


def alterar_reserva_apto():
    cod_res = input("Reserva: ").strip()
    cod_apa = input("Apartamento: ").strip()
    
    linhas = ler_arquivo('reserva_apartamentos.txt')
    nova, achou = [], False

    for linha in linhas:
        ra = parse_reserva_apto(linha)
        if ra['cod_res'] == cod_res and ra['cod_apa'] == cod_apa:
            achou = True
            print("Atual:", ra)
            data_entrada = input("Nova entrada (YYYY-MM-DD): ").strip()
            data_saida = input("Nova saída (YYYY-MM-DD): ").strip()

            if data_entrada:
                ra['data_entrada'] = datetime.strptime(data_entrada, '%Y-%m-%d').date()
            if data_saida:
                ra['data_saida'] = datetime.strptime(data_saida, '%Y-%m-%d').date()

            # Verifica se entrada é antes da saída
            if ra['data_entrada'] >= ra['data_saida']:
                print("❌ Data de entrada deve ser anterior à data de saída.")
                return

            # Verifica conflitos (ignorando a reserva atual)
            if verifica_conflito_reserva(cod_apa, ra['data_entrada'], ra['data_saida'], cod_res):
                print("❌ Não é possível alterar a reserva devido a conflito de datas.")
                return

            nova.append(format_reserva_apto(ra))
        else:
            nova.append(linha)

    if not achou:
        print("❌ Reserva de apartamento não encontrada.")
    else:
        gravar_arquivo('reserva_apartamentos.txt', nova)
        print("✅ Reserva de apartamento alterada com sucesso.")


def excluir_reserva_apto():
    cod_res = input("Reserva: ").strip()
    cod_apa = input("Apartamento: ").strip()
    linhas = ler_arquivo('reserva_apartamentos.txt')
    nova, achou = [], False
    for linha in linhas:
        ra = parse_reserva_apto(linha)
        if ra['cod_res']==cod_res and ra['cod_apa']==cod_apa:
            achou = True
            print("Excluindo:", ra)
            if input("Confirmar? (S/N): ").strip().upper() != 'S':
                nova.append(linha)
        else:
            nova.append(linha)
    if not achou:
        print("Não encontrada.")
    else:
        gravar_arquivo('reserva_apartamentos.txt', nova)
        print("Conclusão.")

def submenu_reserva_apto():
    while True:
        print("\n" + "─"*45)
        print("       GERENCIAMENTO DE RESERVA-APARTAMENTO")
        print("─"*45)
        print("│  1 │ Listar Todas as Reservas de Apartamento")
        print("│  2 │ Buscar Reserva de Apartamento Específica")
        print("│  3 │ Criar Nova Reserva de Apartamento")
        print("│  4 │ Alterar Reserva de Apartamento")
        print("│  5 │ Excluir Reserva de Apartamento")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*45)
        
        opcao = input("Digite sua opção [0-5]: ").strip()
        
        if opcao == '1':
            listar_reservas_apto()
          
            
        elif opcao == '2':
            cod_res = input("\n📋 Digite o código da reserva: ").strip()
            cod_apa = input("\n📋 Digite o código do apartamento: ").strip()
            if cod_res and cod_apa:
                reserva_apto = buscar_reserva_apto(cod_res, cod_apa)
                if reserva_apto:
                    print(f"\n✅ Reserva de apartamento encontrada:")
                    for key, value in reserva_apto.items():
                        print(f"{key.capitalize()}: {value}")
                else:
                    print("\n❌ Reserva de apartamento não encontrada.")
            else:
                print("\n⚠️  Código não pode estar vazio.")

            #Input para continuar, mantendo a informação na tela como foco
            input("\nPressione ENTER para continuar...")
           
            
        elif opcao == '3':
            incluir_reserva_apto()
           
            
        elif opcao == '4':
            alterar_reserva_apto()
           
            
        elif opcao == '5':
            excluir_reserva_apto()
           
            
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
            
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")













# =============== Relatórios =========================
def relatorio_reservas_por_apartamento():
    codigo = input("Código do apto: ").strip()
    reservas_apartamento = ler_arquivo('reserva_apartamentos.txt')
    relatorio = []
    
    for linha in reservas_apartamento:
        ra = parse_reserva_apto(linha)
        if ra['cod_apa'] == codigo:
            relatorio.append(linha)
    
    if not relatorio:
        print("Nenhuma reserva encontrada para o código informado.")
        return
    
    nome = f"relatorio_reservas_apto_{codigo}.txt"
    gravar_arquivo(nome, relatorio)
    print(f"Gerado: {nome}")

def imprimir_relatorio_reservas_apartamento():
    codigo = input("Código do apartamento para leitura do relatório: ").strip()
    nome = f"relatorio_reservas_apto_{codigo}.txt"

    try:
        relatorio = ler_arquivo(nome)
        if not relatorio:
            print("O relatório está vazio.")
            return

        print(f"\nRelatório de Reservas - Apartamento {codigo}")
        print("=" * 50)

        for linha in relatorio:
            partes = linha.strip().split(';')

            reserva = buscar_reserva(partes[0])  # busca a reserva pelo código
            apartamento = buscar_apartamento(partes[1])  # busca o apartamento pelo código

            print("Reserva:")
            print(f"  Código da Reserva: {partes[0]}")
            print(f"  CPF do cliente: {reserva['cpf']}")
            print(f"  Apartamento: {partes[1]}")
            print(f"  Data de Entrada: {partes[2]}")
            print(f"  Data de Saída: {partes[3]}")
            print(f"  Valor: {apartamento['valor']}")
            print("-" * 30)

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")



def relatorio_reservas_por_cliente():
    cpf = input("CPF do cliente: ").strip()
    reservas = ler_arquivo('reservas.txt')
    reservas_cliente_cod = [] # Lista para armazenar os códigos das reservas do cliente
    for linha in reservas:
        reserva = parse_reserva(linha) # Pega o código e o CPF da reserva
        if reserva['cpf'] == cpf:
            reservas_cliente_cod.append(reserva['codigo'])

    reservas_apartamento = ler_arquivo('reserva_apartamentos.txt')
    relatorio = []
    for linha in reservas_apartamento:
        cod_reserva_apto = (linha.split(';'))[0] # Pega o código da reserva do apartamento
        if cod_reserva_apto in reservas_cliente_cod:
            relatorio.append(linha)

    nome = f"relatorio_reservas_cliente_{cpf}.txt"

    gravar_arquivo(nome, relatorio)
    print(f"Gerado: {nome}")

def imprimir_relatorio_reservas_cliente():
    cpf = input("CPF do cliente para leitura do relatório: ").strip()
    nome = f"relatorio_reservas_cliente_{cpf}.txt"

    try:
        relatorio = ler_arquivo(nome)
        if not relatorio:
            print("O relatório está vazio.")
            return

        print(f"\nRelatório de Reservas - Cliente {cpf}")
        print("=" * 50)

        for linha in relatorio:
            partes = linha.strip().split(';')

            reserva = buscar_reserva(partes[0])  # busca a reserva pelo código
            apartamento = buscar_apartamento(partes[1])  # busca o apartamento pelo código

            print("Reserva:")
            print(f"  Código da Reserva: {partes[0]}")
            print(f"  CPF do cliente: {reserva['cpf']}")
            print(f"  Apartamento: {partes[1]}")
            print(f"  Data de Entrada: {partes[2]}")
            print(f"  Data de Saída: {partes[3]}")
            print(f"  Valor: {apartamento['valor']}")
            print("-" * 30)

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def relatorio_reservas_por_periodo():
    try:
        data_inicio = datetime.strptime(input("Data inicial (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()
        data_fim = datetime.strptime(input("Data final (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()

        if data_fim < data_inicio:
            print("Erro: a data final não pode ser anterior à data inicial.")
            return

        reservas_apartamento = ler_arquivo('reserva_apartamentos.txt')
        encontrou = False
        relatorio = []

        for linha in reservas_apartamento:
            reserva_apto = parse_reserva_apto(linha)

            data_ent = reserva_apto['data_entrada']
            data_sai = reserva_apto['data_saida']

            if (data_inicio <= data_ent <= data_fim) or (data_inicio <= data_sai <= data_fim):
                reserva = buscar_reserva(reserva_apto['cod_res'])
                apartamento = buscar_apartamento(reserva_apto['cod_apa'])
                cliente = buscar_cliente((reserva['cpf']))

                if reserva is None or apartamento is None:
                    continue
                
                relatorio.append(f"{reserva_apto['cod_res']};{cliente['nome']};{reserva['cpf']};{reserva_apto['cod_apa']};{reserva_apto['data_entrada'].isoformat()};{reserva_apto['data_saida'].isoformat()};{apartamento['valor']}")
                encontrou = True

        if not encontrou:
            print("Nenhuma reserva encontrada no período informado.")

        nome = f"relatorio_reservas_do_periodo_{data_inicio}_{data_fim}.txt"
        gravar_arquivo(nome, relatorio)
        print(f"Gerado: {nome}")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def imprimir_relatorio_por_periodo():
    data_inicio = datetime.strptime(input("Data inicial (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()
    data_fim = datetime.strptime(input("Data final (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()

    if data_fim < data_inicio:
        print("Erro: a data final não pode ser anterior à data inicial.")
        return
    nome = f"relatorio_reservas_do_periodo_{data_inicio}_{data_fim}.txt"

    try:
        relatorio = ler_arquivo(nome)
        if not relatorio:
            print("O relatório está vazio.")
            return

        print(f"\nRelatório por Período de {data_inicio} até {data_fim}")
        print("=" * 50)
        for linha in relatorio:
            partes = linha.strip().split(';')
            print("Reserva:")
            print(f"  Código da Reserva: {partes[0]}")
            print(f"  Nome do Cliente: {partes[1]}")
            print(f"  CPF do cliente: {partes[2]}")
            print(f"  Apartamento: {partes[3]}")
            print(f"  Data de Entrada: {partes[4]}")
            print(f"  Data de Saída: {partes[5]}")
            print(f"  Valor: {partes[6]}")
            print("-" * 30)
            encontrou = True

        if not encontrou:
            print("Nenhuma reserva encontrada no período informado.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")



def submenu_relatorios():
    while True:
        print("\n" + "─"*45)
        print("           RELATÓRIOS E CONSULTAS")
        print("─"*45)
        print("│  1 │ Criar Relatório de Reservas por Apartamento")
        print("│  2 │ Criar Relatório de Reservas por Cliente")
        print("│  3 │ Criar Relatório de REservas por Período de Reserva")
        print("│  4 │ Imprimir Relatório de Reservas por Apartamento")
        print("│  5 │ Imprimir Relatório de Reservas por Cliente")
        print("│  6 │ Imprimir Relatório de Período de Reserva")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*45)
        
        opcao = input("Digite sua opção [0-6]: ").strip()
        
        if opcao == '1':
            relatorio_reservas_por_apartamento()
      
            
        elif opcao == '2':
            relatorio_reservas_por_cliente()
    
        elif opcao == '3':
            relatorio_reservas_por_periodo()
        
        elif opcao == '4':
            imprimir_relatorio_reservas_apartamento()

        elif opcao == '5':
            imprimir_relatorio_reservas_cliente()
        
        elif opcao == '6':
            imprimir_relatorio_por_periodo()
            
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
        print("│  4 │ Gerenciar Reserva-Apartamento")
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
