menu = '''
        [0] - Saque
        [1] - Depósito
        [2] - Extrato
        [3] - Sair do sistema'''
opcoes = [0,1,2,3]
depositos = []
saques_realizados = []
saque_diario = 0
LIMITE_SAQUE = 500
LIMITE_SAQUE_DIARIO = 3
saldo_conta = 0

while True:
    escolha = int(input(f"Bem-vindo ao Banco V1. Por favor digite uma opção válida: \n{menu}\n"))
    if escolha not in opcoes:
        escolha = int(input(f"Opção inválida! Por favor escolha uma opção válida: \n{menu}\n"))
        if escolha == 3:
            print("Obrigado por utilizar o Banco V1! Volte Sempre!")
            break
    elif escolha == 3:
        print("Obrigado por utilizar o Banco V1! Volte Sempre!")
        break
    
    #SAQUE
    if escolha == 0:
        if saque_diario >= 3:
            print(f"Seu limite de saques diários foi atingido!")
        elif saldo_conta == 0:
            print("Você não tem saldo para saque, escolha outra opção.")
        elif saque_diario < 3:
            valor_saque = int(input("Qual valor você deseja sacar: "))
            while valor_saque <= 0:
                valor_saque = int(input("Valor incorreto. Digite novamente: "))
            while valor_saque > LIMITE_SAQUE:
                valor_saque = int(input(f"Valor solicitado para saque excede o limite diário de R${LIMITE_SAQUE:.2f}!"
                                        "Escolha um valor válido para saque:\n"))
            while valor_saque > saldo_conta:
                valor_saque = int(input(f"Saldo de R$ {saldo_conta} insuficiente para saque! Por favor, escolha outro valor:\n"))
            if valor_saque <= LIMITE_SAQUE and valor_saque <= saldo_conta:
                saldo_conta -= valor_saque
                saques_realizados.append(valor_saque)
                saque_diario += 1
                print(f"Valor de R$ {valor_saque:.2f} autorizado para saque, retire seu dinheiro!")
                if escolha == 3:
                    print("Obrigado por utilizar o Banco V1! Volte Sempre!")
                    break
   
    #DEPÓSITO
    if escolha == 1:
        valor_deposito = float(input("Digite o valor para depósito: "))
        while valor_deposito <= 0:
            valor_deposito = float(input("Valor inválido. Digite um valor válido para depósito: "))
        depositos.append(valor_deposito)
        saldo_conta += valor_deposito
        print(f"Valor de R$ {valor_deposito:.2f} depositado com sucesso!!")
        if escolha == 3:
            print("Obrigado por utilizar o Banco V1! Volte Sempre!")
            break
   
    #EXTRATO
    if escolha == 2:
        mensagem = "Aqui está o seu extrato bancário"
        print(mensagem.upper().center(len(mensagem)+8, "-"))
        if len(depositos) == 0 and len(saques_realizados) == 0:
            print("Não foram realizadas movimentações em sua conta.")
        else:
            print("Depósitos Realizados:")
            if len(depositos) == 0:
                print("Sem depósitos realizados.")
            else:
                for d in depositos:
                    print(f"R$ {d:.2f}")
            print("Valores Resgatados:")
            if len(saques_realizados) == 0:
                print("Sem saques realizados.")
            else:
                for s in saques_realizados:
                    print(f"R$ {s:.2f}")
            print(f"Limite de Saques diário: 0{LIMITE_SAQUE_DIARIO}\n"
                  f"Saques realizados: 0{saque_diario}\n"
                  f"Saldo em conta: {saldo_conta}")