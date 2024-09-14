from datetime import date, time, datetime

# FUNÇÃO CRIAR USUÁRIO
def criar_usuario(usuarios):
    cpf = (input("Digite o CPF (somente números): "))
    filtro = [usuario for usuario in usuarios if usuario['cpf']==cpf]
    if filtro:
        print("CPF já cadastrado!")
    else:
        nome = input("Digite o nome completo: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (Rua, nº, bairro, cidade/UF): ")
        usuarios.append({"cpf": cpf, "nome": nome, "data_nasc": data_nascimento, "Endereco": endereco})
    return usuarios
# FUNÇÃO SAQUE
def saque(*, valor_saque, saldo_conta, saques_realizados, data_hora_saques, LIMITE_SAQUE, LIMITE_SAQUE_DIARIO, saque_diario, transacoes):
    saque_excedido = valor_saque > saldo_conta
    valor_saque_excedido = valor_saque > LIMITE_SAQUE
    limite_saques_excedidos = saque_diario >= LIMITE_SAQUE_DIARIO
    # VALIDAÇÕES PARA SAQUE
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
    # REALIZAÇÃO DO PROCEDIMENTO DE SAQUE
    else:
        saldo_conta -= valor_saque
        saques_realizados.append(valor_saque)
        data_hora_saques.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        saque_diario += 1
        transacoes += 1
        print(f"Valor de R$ {valor_saque:.2f} autorizado para saque, retire seu dinheiro!")
    # RETORNO DAS VARIÁVEIS PARA FUNÇÃO PRINCIPAL
    return saldo_conta, saques_realizados, data_hora_saques, saque_diario, transacoes
# FUNÇÃO DEPÓSITO
def deposito(*, valor_deposito, depositos, data_hora_depositos, saldo_conta, transacoes):
    # VALIDAÇÕES PARA A FUNÇÃO DE DEPÓSITO
    while valor_deposito <= 0:
        valor_deposito = float(input("Valor inválido. Digite um valor válido para depósito: "))
    if transacoes >= 10:
        print("Limite de transações diárias excedido!")
    # REALIZAÇÃO DA OPERAÇÃO DE DEPÓSITO
    else:
        depositos.append(valor_deposito)
        data_hora_depositos.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        saldo_conta += valor_deposito
        transacoes += 1
        print(f"Valor de R$ {valor_deposito:.2f} depositado com sucesso!!")
    # RETORNO DAS VARIÁVEIS PARA A FUNÇÃO PRINCIPAL DO SISTEMA
    return saldo_conta, depositos, data_hora_depositos, transacoes
# FUNÇÃO EXTRATO
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
    print(f"Transações Realizadas: {transacoes}")
# FUNÇÃO PRINCIPAL DO SISTEMA
def run():
    usuarios = []
    depositos = []
    data_hora_depositos = []
    saques_realizados = []
    data_hora_saques = []
    saque_diario = 0
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
        [5] - Sair do sistema'''

    while True:
        escolha = int(input(f"Bem-vindo ao Banco V1. Por favor digite uma opção válida: \n{menu}\n"))
        if escolha < 0 or escolha > 5:
            print(f"Opção inválida!")
            if escolha == 3:
                print("Obrigado por utilizar o Banco V1! Volte Sempre!")
                break
        # CRIAR USUÁRIO
        elif escolha == 0:
            usuarios = criar_usuario(usuarios)
        # SAQUE
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
        #SAÍDA DO SISTEMA
        elif escolha == 5:
            print("Obrigado por utilizar o Banco V1! Volte Sempre!")
            break

run()