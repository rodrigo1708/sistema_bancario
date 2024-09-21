from datetime import date, time, datetime

#FUNÇÃO PARA CRIAR USUÁRO
def criar_usuario(usuarios):
    cpf = (input("Digite o CPF (somente números): "))
    filtro = filtro_usuarios(cpf, usuarios)
    if filtro:
        print("CPF já cadastrado!")
    else:
        nome = input("Digite o nome completo: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (Rua, nº, bairro, cidade/UF): ")
        usuarios.append({"cpf": cpf, "nome": nome, "data_nasc": data_nascimento, "Endereco": endereco})
        print("Usuário cadastrado com sucesso!")
    return cpf, usuarios

#FUNÇÃO PARA FILTRAR USUÁRIOS JÁ CADASTRADOS NO SISTEMA
def filtro_usuarios(cpf, usuarios):
    filtro = [usuario for usuario in usuarios if usuario['cpf']==cpf]
    return filtro[0] if filtro else None

#FUNÇÃO PARA CRIAR CONTA
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = (input("Digite o CPF (somente números): "))
    filtro = filtro_usuarios(cpf, usuarios)
    if filtro:
        print("Conta Criada com sucesso!")
        contas.append({"agencia":agencia, "numero_conta": numero_conta, "usuario": filtro})
        return contas
    else:
        print("Usuário não cadastro, não é possível criar a conta!")

#FUNÇÃO PARA LISTAR CONTAS CADASTRADAS
def listar_contas(contas):
    for conta in contas:
        print(f'Titular: {conta["usuario"]["nome"]}\nAgência: {conta["agencia"]}. Conta: {conta["numero_conta"]}')

#FUNÇÃO PARA SAQUE
def saque(*, valor_saque, saldo_conta, saques_realizados, data_hora_saques, LIMITE_SAQUE, LIMITE_SAQUE_DIARIO, saque_diario, transacoes):
    saque_excedido = valor_saque > saldo_conta
    valor_saque_excedido = valor_saque > LIMITE_SAQUE
    limite_saques_excedidos = saque_diario >= LIMITE_SAQUE_DIARIO
    if transacoes >= 10:
        print("Limite de transações diárias excedido!")
    elif saque_excedido:
        print("Você não tem saldo para saque, escolha outra opção.")
    elif valor_saque_excedido:
        print(f"Valor solicitado para saque excede o limite diário de R$ {LIMITE_SAQUE}.")
    elif limite_saques_excedidos:
        print("Limite de saques diários já foi atingido!")
    elif valor_saque < 0:
        print("Valor solicitado inválido!")
    else:
        saldo_conta -= valor_saque
        saques_realizados.append(valor_saque)
        data_hora_saques.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        saque_diario += 1
        transacoes += 1
        print(f"Valor de R$ {valor_saque:.2f} autorizado para saque, retire seu dinheiro!")
    return saldo_conta, saques_realizados, data_hora_saques, saque_diario, transacoes

#FUNÇÃO PARA DEPÓSITO
def deposito(*, valor_deposito, depositos, data_hora_depositos, saldo_conta, transacoes):
    while valor_deposito <= 0:
        valor_deposito = float(input("Valor inválido. Digite um valor válido para depósito: "))
    if transacoes >= 10:
        print("Limite de transações diárias excedido!")
    else:
        depositos.append(valor_deposito)
        data_hora_depositos.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        saldo_conta += valor_deposito
        transacoes += 1
        print(f"Valor de R$ {valor_deposito:.2f} depositado com sucesso!!")
    return saldo_conta, depositos, data_hora_depositos, transacoes

#FUNÇÃO PARA VISUALIZAR O EXTRATO
def extrato(saldo_conta, depositos, data_hora_depositos, saques_realizados, data_hora_saques, saque_diario, LIMITE_SAQUE_DIARIO, transacoes):
    mensagem = "Aqui está o seu extrato bancário"
    print(mensagem.upper().center(len(mensagem) + 8, "-"))
    
    if len(depositos) == 0 and len(saques_realizados) == 0:
        print("Não foram realizadas movimentações em sua conta.")
    else:
        print("Depósitos Realizados:")
        if len(depositos) == 0:
            print("Sem depósitos realizados.")
        else:
            for i, d in enumerate(depositos):
                print(f'{i+1} - R$ {d:.2f}. Data e Hora da Transação: {data_hora_depositos[i]}')
        print("Saques Realizados:")
        if len(saques_realizados) == 0:
            print("Sem saques realizados.")
        else:
            for i, s in enumerate(saques_realizados):
                print(f'{i+1} - R$ {s:.2f}. Data e Hora da Transação: {data_hora_saques[i]}')
    
    print(f"Limite de Saques diário: {LIMITE_SAQUE_DIARIO}")
    print(f"Saques realizados: {saque_diario}")
    print(f"Saldo em conta: R$ {saldo_conta:.2f}")
    print(transacoes)

#FUNÇÃO PRINCIPAL DO SISTEMA
def run():
    usuarios = []
    contas = []
    numero_conta = 0
    depositos = []
    data_hora_depositos = []
    saques_realizados = []
    data_hora_saques = []
    saque_diario = 0
    AGENCIA = "0001"
    LIMITE_SAQUE = 500
    LIMITE_SAQUE_DIARIO = 3
    saldo_conta = 0
    transacoes = 0

    menu = '''
        [0] - Criar usuário
        [1] - Criar conta
        [2] - Saque
        [3] - Depósito
        [4] - Extrato
        [5] - Listar contas
        [6] - Sair do sistema'''

    while True:
        escolha = int(input(f"Bem-vindo ao Banco V1. Por favor digite uma opção válida: \n{menu}\n"))
        if escolha < 0 or escolha > 6 :
            print(f"Opção inválida!")
            if escolha == 3:
                print("Obrigado por utilizar o Banco V1! Volte Sempre!")
                break
        #CRIAR USUÁRIO
        elif escolha == 0:
            uusarios = criar_usuario(usuarios)
        #CRIAR CONTA
        elif escolha == 1:
            numero_conta += 1
            contas = criar_conta(AGENCIA, numero_conta, usuarios, contas)
        #SAQUE
        elif escolha == 2:
            valor_saque = float(input("Digite o valor para saque: "))   
            saldo_conta, saques_realizados, data_hora_saques, saque_diario, transacoes= saque(
                valor_saque=valor_saque,
                saldo_conta=saldo_conta,
                saques_realizados=saques_realizados,
                data_hora_saques=data_hora_saques,
                LIMITE_SAQUE=LIMITE_SAQUE,
                LIMITE_SAQUE_DIARIO=LIMITE_SAQUE_DIARIO,
                saque_diario=saque_diario,
                transacoes=transacoes)
        #DEPÓSITOS
        elif escolha == 3:
            valor_deposito = float(input("Digite o valor para depósito: "))
            saldo_conta, depositos, data_hora_depositos, transacoes = deposito(
                valor_deposito=valor_deposito,
                depositos=depositos,
                data_hora_depositos=data_hora_depositos,
                saldo_conta=saldo_conta,
                transacoes=transacoes)
        #EXTRATOS
        elif escolha == 4:
            extrato(saldo_conta, depositos, data_hora_depositos, saques_realizados, data_hora_saques, saque_diario, LIMITE_SAQUE_DIARIO, transacoes)
        #LISTAR CONTAS
        elif escolha == 5:
            listar_contas(contas)
        #SAÍDA DO SISTEMA
        elif escolha == 6:
            print("Obrigado por utilizar o Banco V1! Volte Sempre!")
            break

run()