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

def carregar_clientes(cliente_arquivo='clientes.txt'):
    linhas = ler_arquivo(cliente_arquivo)
    clientes = []
    for l in linhas:
        cliente = parse_cliente(l)
        if cliente is not None:
            clientes.append(cliente)
    return clientes

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

        nome = input("\nNovo Nome (ENTER para manter): ").strip() or cliente['nome']
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
    print("\nVai excluir:")
    for k, v in cliente.items():
        print(f"{k.capitalize()}: {v}")
    confirm = input("\nTem certeza que deseja excluir este cliente? (S/N): ").strip().upper()
    if confirm == 'S':
        clientes.remove(cliente)
        print("Cliente excluído")
    else:
        print("Exclusão cancelada.")

def submenu_clientes():
  clientes_arquivo= 'clientes.txt'
  clientes = carregar_clientes(clientes_arquivo)

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
  if gravar_arquivo(clientes_arquivo, novas_linhas):
        print("Alterações salvas em arquivo.")
  else:
        print("Falha ao salvar alterações.")


# =============== Reservas =========================

def parse_reserva(linha):
    codigo, cpf = linha.split(';')
    return {'codigo': codigo, 'cpf': cpf}

def format_reserva(r):
    return f"{r['codigo']};{r['cpf']}"

def carregar_reservas(reserva_arquivo='reservas.txt'):
    linhas = ler_arquivo(reserva_arquivo)
    reservas = []
    for l in linhas:
        reserva = parse_reserva(l)
        if reserva is not None:
            reservas.append(reserva)
    return reservas

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
    print("\nDados atuais da reserva:")
    print(f"Código: {r['codigo']}, CPF: {r['cpf']}\n")
    novo_cpf = input("Novo CPF do cliente (ENTER para manter): ").strip() or r['cpf']
    encontrado = False
    for c in clientes:
        if c['cpf'] == novo_cpf:
            encontrado = True
            break
    if not encontrado:
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
    print("\nExcluindo reserva:")
    print(f"Código: {r['codigo']}, CPF: {r['cpf']}\n")
    if input("Confirmar exclusão (S/N): ").strip().upper() == 'S':
        reservas.remove(r)
        print("Reserva excluída em memória.")
    else:
        print("Cancelado.")

def submenu_reservas():
    reserva_arquivo = 'reservas.txt'
    reservas = carregar_reservas(reserva_arquivo)

    clientes_arquivo= 'clientes.txt'
    clientes = carregar_clientes(clientes_arquivo)

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

def carregar_apartamentos(arquivo='apartamentos.txt'):
    linhas = ler_arquivo(arquivo)
    apartamentos = []
    for linha in linhas:
        apartamento = parse_apartamento(linha)
        if apartamento:
            apartamentos.append(apartamento)
    return apartamentos

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
            print("\nDados atuais:")
            print(f"Código: {a['codigo']}")
            print(f"Descrição: {a['descricao']}")
            print(f"Capacidade: {a['adultos']} adulto(s), {a['criancas']} criança(s)")
            print(f"Valor por dia: R$ {a['valor']:.2f}\n")

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
            print("\nExcluir:")
            print(f"Código: {a['codigo']}")
            print(f"Descrição: {a['descricao']}")
            print(f"Capacidade: {a['adultos']} adulto(s), {a['criancas']} criança(s)")
            print(f"Valor por dia: R$ {a['valor']:.2f}\n")
            if input("Confirmar? (S/N): ").strip().upper() == 'S':
                apartamentos.remove(a)
                print("✅ Apartamento excluído com sucesso.")
            else:
                print("❌ Exclusão cancelada.")
            break
    if not achou:
        print("❌ Apartamento não encontrado.")


def submenu_apartamentos():
    
    apartamentos = carregar_apartamentos('apartamentos.txt')

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
def verifica_conflito_reserva(reservas_apto, cod_apa, nova_entrada, nova_saida, cod_res=None):
    for ra in reservas_apto:
        if ra['cod_apa'] == cod_apa:
            if cod_res and ra['cod_res'] == cod_res:
                continue
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

def carregar_reservas_apto(arquivo='reserva_apartamentos.txt'):
    linhas = ler_arquivo(arquivo)
    reservas_apto = []
    for linha in linhas:
        reserva_apto = parse_reserva_apto(linha)
        reservas_apto.append(reserva_apto)
    return reservas_apto

def format_reserva_apto(r):
    return f"{r['cod_res']};{r['cod_apa']};{r['data_entrada'].isoformat()};{r['data_saida'].isoformat()}"

def listar_reservas_apto(reservas_apto):
    if not reservas_apto:
        print("Sem reservas de apartamento.")
    else:
        for ra in reservas_apto:
            print(f"Reserva: {ra['cod_res']}, Apartamento: {ra['cod_apa']}, Entrada: {ra['data_entrada'].strftime('%d/%m/%Y')}, Saída: {ra['data_saida'].strftime('%d/%m/%Y')}")

def buscar_reserva_apto(reservas_apto, cod_res, cod_apa):
    for ra in reservas_apto:
        if ra['cod_res'] == cod_res and ra['cod_apa'] == cod_apa:
            return ra
    return None

def incluir_reserva_apto(reservas_apto, reservas, apartamentos):
    cod_res = input("Código da reserva: ").strip()
    
    # verifica se existe alguma reserva com o código informado
    existe_reserva = False
    for r in reservas:
        if r['codigo'] == cod_res:
            existe_reserva = True
            break

    if not existe_reserva:
        print("❌ Não existe uma reserva com esse código.")
        return reservas_apto

    cod_apa = input("Código do apartamento: ").strip()

    # verifica se o apartamento existe
    existe_apartamento = False
    for a in apartamentos:
        if a['codigo'] == cod_apa:
            existe_apartamento = True
            break

    if not existe_apartamento:
        print("❌ Não existe um apartamento com esse código.")
        return reservas_apto

    # Verifica se já existe uma reserva para o mesmo código e apartamento
    if buscar_reserva_apto(reservas_apto, cod_res, cod_apa):
        print("❌ Já existe uma reserva com esse código e apartamento.")
        return reservas_apto

    data_entrada = datetime.strptime(input("Entrada (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()
    data_saida = datetime.strptime(input("Saída (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()

    if data_entrada >= data_saida:
        print("❌ Data de entrada deve ser anterior à data de saída.")
        return reservas_apto

    if verifica_conflito_reserva(reservas_apto, cod_apa, data_entrada, data_saida):
        print("❌ Não é possível realizar a reserva devido a conflito de datas.")
        return reservas_apto

    ra = {
        'cod_res': cod_res,
        'cod_apa': cod_apa,
        'data_entrada': data_entrada,
        'data_saida': data_saida
    }
    reservas_apto.append(ra)
    print("✅ Reserva de apartamento incluída com sucesso.")
    return reservas_apto

def alterar_reserva_apto(reservas_apto):
    cod_res = input("Reserva: ").strip()
    cod_apa = input("Apartamento: ").strip()
    
    for ra in reservas_apto:
        if ra['cod_res'] == cod_res and ra['cod_apa'] == cod_apa:
            print("\nAtualizando reserva com os seguintes dados:")
            print(f"Código da reserva: {ra['cod_res']}")
            print(f"Código do apto: {ra['cod_apa']}")
            print(f"Data de entrada: {ra['data_entrada'].strftime('%d/%m/%Y')}")
            print(f"Data de saída: {ra['data_saida'].strftime('%d/%m/%Y')}\n")
            data_entrada = input("Nova entrada (YYYY-MM-DD): ").strip()
            data_saida = input("Nova saída (YYYY-MM-DD): ").strip()

            # variáveis temporárias
            nova_entrada = ra['data_entrada']
            nova_saida = ra['data_saida']

            if data_entrada:
                nova_entrada = datetime.strptime(data_entrada, '%Y-%m-%d').date()
            if data_saida:
                nova_saida = datetime.strptime(data_saida, '%Y-%m-%d').date()

            if nova_entrada >= nova_saida:
                print("❌ Data de entrada deve ser anterior à data de saída.")
                return reservas_apto

            if verifica_conflito_reserva(reservas_apto, cod_apa, nova_entrada, nova_saida, cod_res):
                print("❌ Não é possível alterar a reserva devido a conflito de datas.")
                return reservas_apto

            # Se tudo ok, atualiza diretamente
            ra['data_entrada'] = nova_entrada
            ra['data_saida'] = nova_saida
            print("✅ Reserva de apartamento alterada com sucesso.")
            return reservas_apto

    print("❌ Reserva de apartamento não encontrada.")
    return reservas_apto

def excluir_reserva_apto(reservas_apto):
    cod_res = input("Reserva: ").strip()
    cod_apa = input("Apartamento: ").strip()
    achou = False
    for ra in reservas_apto[:]:  # iterar sobre cópia da lista
        if ra['cod_res'] == cod_res and ra['cod_apa'] == cod_apa:
            achou = True
            print("\nExcluindo reserva com os seguintes dados:")
            print(f"Código da reserva: {ra['cod_res']}")
            print(f"Código do apto: {ra['cod_apa']}")
            print(f"Data de entrada: {ra['data_entrada'].strftime('%d/%m/%Y')}")
            print(f"Data de saída: {ra['data_saida'].strftime('%d/%m/%Y')}\n")
            if input("Confirmar? (S/N): ").strip().upper() == 'S':
                reservas_apto.remove(ra)
                print("✅ Reserva excluída com sucesso.")
            else:
                print("❌ Exclusão cancelada.")
            break
    if not achou:
        print("❌ Reserva não encontrada.")

def submenu_reserva_apto():
    reservas_apto = carregar_reservas_apto('reserva_apartamentos.txt')

    reservas = carregar_reservas('reservas.txt')

    apartamentos = carregar_apartamentos('apartamentos.txt')

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
            listar_reservas_apto(reservas_apto)
            input("\nPressione ENTER para continuar...")

        elif opcao == '2':
            cod_res = input("\n📋 Digite o código da reserva: ").strip()
            cod_apa = input("\n📋 Digite o código do apartamento: ").strip()
            if cod_res and cod_apa:
                reserva_apto = buscar_reserva_apto(reservas_apto, cod_res, cod_apa)
                if reserva_apto:
                    print(f"\n✅ Reserva de apartamento encontrada:")
                    for key, value in reserva_apto.items():
                        print(f"{key.capitalize()}: {value}")
                else:
                    print("\n❌ Reserva de apartamento não encontrada.")
            else:
                print("\n⚠️  Código não pode estar vazio.")
            input("\nPressione ENTER para continuar...")

        elif opcao == '3':
            incluir_reserva_apto(reservas_apto, reservas, apartamentos)

        elif opcao == '4':
            alterar_reserva_apto(reservas_apto)

        elif opcao == '5':
            excluir_reserva_apto(reservas_apto)

        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            lista_reservas_formatadas = []
            for ra in reservas_apto:
                lista_reservas_formatadas.append(format_reserva_apto(ra))

            gravar_arquivo('reserva_apartamentos.txt', lista_reservas_formatadas)
            break

        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 5.")
            input("Pressione ENTER para continuar...")


# =============== Relatórios =========================
def relatorio_reservas_por_apartamento(reservas_apto):
    codigo = input("Código do apartamento: ").strip()
    relatorio = []
    
    for ra in reservas_apto:
        if ra['cod_apa'] == codigo:
            relatorio.append(f"{ra['cod_res']};{ra['cod_apa']};{ra['data_entrada']};{ra['data_saida']}")

    if not relatorio:
        print("Nenhuma reserva encontrada para o código informado.")
        return

    nome = f"relatorio_reservas_apto_{codigo}.txt"
    gravar_arquivo(nome, relatorio)
    print(f"Gerado: {nome}")

def imprimir_relatorio_reservas_apartamento(reservas, apartamentos):
    codigo = input("Código do apartamento para leitura do relatório: ").strip()
    if not buscar_apartamento(codigo, apartamentos):
        print("Apartamento não encontrado.")
        return
    
    nome = f"relatorio_reservas_apto_{codigo}.txt"

    try:
        relatorio = ler_arquivo(nome)
        if not relatorio:
            print("O relatório não existe ou está vazio.")
            return

        print(f"\nRelatório de Reservas - Apartamento {codigo}")
        print("=" * 50)

        for linha in relatorio:
            partes = linha.strip().split(';')
            reserva = buscar_reserva(partes[0], reservas )
            apartamento = buscar_apartamento(partes[1], apartamentos)

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

def relatorio_reservas_por_cliente(reservas, reservas_apto):
    cpf = input("CPF do cliente: ").strip()

    if not buscar_cliente(cpf, reservas):
        print("Cliente não encontrado.")
        return
    
    reservas_cliente_cod = []
    for r in reservas:
        if r['cpf'] == cpf:
            reservas_cliente_cod.append(r['codigo'])

    relatorio = []
    for ra in reservas_apto:
        if ra['cod_res'] in reservas_cliente_cod:
            relatorio.append(f"{ra['cod_res']};{ra['cod_apa']};{ra['data_entrada']};{ra['data_saida']}")

    nome = f"relatorio_reservas_cliente_{cpf}.txt"
    gravar_arquivo(nome, relatorio)
    print(f"Gerado: {nome}")

def imprimir_relatorio_reservas_cliente(reservas, apartamentos):
    cpf = input("CPF do cliente para leitura do relatório: ").strip()
    nome = f"relatorio_reservas_cliente_{cpf}.txt"

    try:
        relatorio = ler_arquivo(nome)
        if not relatorio:
            print("O relatório não existe ou está vazio.")
            return

        print(f"\nRelatório de Reservas - Cliente {cpf}")
        print("=" * 50)

        for linha in relatorio:
            partes = linha.strip().split(';')
            reserva = buscar_reserva(partes[0], reservas)
            apartamento = buscar_apartamento(partes[1], apartamentos)

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

def relatorio_reservas_por_periodo(clientes, apartamentos, reservas, reservas_apto):
    try:
        data_inicio = datetime.strptime(input("Data inicial (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()
        data_fim = datetime.strptime(input("Data final (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()

        if data_fim < data_inicio:
            print("Erro: a data final não pode ser anterior à data inicial.")
            return

        relatorio = []
        encontrou = False

        for ra in reservas_apto:
            data_ent = ra['data_entrada']
            data_sai = ra['data_saida']

            if (data_inicio <= data_ent <= data_fim) or (data_inicio <= data_sai <= data_fim):
                reserva = buscar_reserva(ra['cod_res'],reservas )
                apartamento = buscar_apartamento(ra['cod_apa'], apartamentos)
                cliente = buscar_cliente(reserva['cpf'],clientes )

                if reserva is None or apartamento is None or cliente is None:
                    continue

                relatorio.append(f"{ra['cod_res']};{cliente['nome']};{reserva['cpf']};{ra['cod_apa']};{data_ent};{data_sai};{apartamento['valor']}")
                encontrou = True

        if not encontrou:
            print("Nenhuma reserva encontrada no período informado.")
            return

        nome = f"relatorio_reservas_do_periodo_{data_inicio}_{data_fim}.txt"
        gravar_arquivo(nome, relatorio)
        print(f"Gerado: {nome}")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def imprimir_relatorio_por_periodo():
    try:
        data_inicio = datetime.strptime(input("Data inicial (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()
        data_fim = datetime.strptime(input("Data final (YYYY-MM-DD): ").strip(), '%Y-%m-%d').date()

        if data_fim < data_inicio:
            print("Erro: a data final não pode ser anterior à data inicial.")
            return

        nome = f"relatorio_reservas_do_periodo_{data_inicio}_{data_fim}.txt"
        relatorio = ler_arquivo(nome)
        if not relatorio:
            print("O relatório não existe ou está vazio.")
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

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def submenu_relatorios():
    # lê tudo uma vez
    clientes = carregar_clientes('clientes.txt')

    apartamentos = carregar_apartamentos('apartamentos.txt')

    reservas = carregar_reservas('reservas.txt')

    reservas_apto = carregar_reservas_apto('reserva_apartamentos.txt')

    while True:
        print("\n" + "─"*45)
        print("           RELATÓRIOS E CONSULTAS")
        print("─"*45)
        print("│  1 │ Criar Relatório de Reservas por Apartamento")
        print("│  2 │ Criar Relatório de Reservas por Cliente")
        print("│  3 │ Criar Relatório de Reservas por Período de Reserva")
        print("│  4 │ Imprimir Relatório de Reservas por Apartamento")
        print("│  5 │ Imprimir Relatório de Reservas por Cliente")
        print("│  6 │ Imprimir Relatório de Período de Reserva")
        print("│  0 │ Voltar ao Menu Principal")
        print("─"*45)
        
        opcao = input("Digite sua opção [0-6]: ").strip()
        
        if opcao == '1':
            relatorio_reservas_por_apartamento(reservas_apto)
        elif opcao == '2':
            relatorio_reservas_por_cliente(reservas, reservas_apto)
        elif opcao == '3':
            relatorio_reservas_por_periodo(clientes, apartamentos, reservas, reservas_apto)
        elif opcao == '4':
            imprimir_relatorio_reservas_apartamento(reservas, apartamentos)
        elif opcao == '5':
            imprimir_relatorio_reservas_cliente(reservas, apartamentos)
        elif opcao == '6':
            imprimir_relatorio_por_periodo()
        elif opcao == '0':
            print("\n🔙 Voltando ao menu principal...")
            break
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 0 e 6.")
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
