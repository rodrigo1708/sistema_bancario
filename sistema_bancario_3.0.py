from datetime import datetime
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        self._LIMITE_SAQUE = 500
        self._LIMITE_SAQUE_DIARIO = 3
        self.depositos = []
        self.data_hora_depositos = []
        self.saques_realizados = []
        self.data_hora_saques = []
        self.saque_diario = 0

    @property
    def saldo(self):
         return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        saque_excedido = valor > self._saldo
        valor_saque_excedido = valor > self._LIMITE_SAQUE
        limite_saques_excedidos = self.saque_diario >= self._LIMITE_SAQUE_DIARIO
        if saque_excedido:
            print("Você não tem saldo para saque, escolha outra opção.")
        elif valor_saque_excedido:
            print(f"Valor solicitado para saque excede o limite diário de R$ {self._LIMITE_SAQUE}.")
        elif limite_saques_excedidos:
            print("Limite de saques diários já foi atingido!")
        elif valor < 0:
            print("Valor solicitado inválido!")
        else:
            self._saldo -= valor
            self.saques_realizados.append(valor)
            self.data_hora_saques.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.saque_diario += 1
            print(f"Valor de R$ {valor:.2f} autorizado para saque, retire seu dinheiro!")
            return True
        return False
    
    def depositar(self, valor):
        while valor <= 0:
            valor = float(input("Valor inválido. Digite um valor válido para depósito: "))
    
        self._saldo += valor
        self.depositos.append(valor)
        self.data_hora_depositos.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print(f"Valor de R$ {valor:.2f} depositado com sucesso!!")
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    def __str__(self):
        return f"Titular: {self.cliente.nome}\nConta: {self.numero}\nAgência: {self.agencia}\nSaldo: R$ {self.saldo:.2f}"

    def sacar(self, valor):
        return super().sacar(valor)

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%s"),
            }
        )

class Transacao (ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

#FUNÇÃO PARA CRIAR USUÁRO
def criar_cliente(clientes):
    cpf = (input("Digite o CPF (somente números): "))
    filtro = filtro_cliente(cpf, clientes)
    if filtro:
        print("CPF já cadastrado!")
    else:
        nome = input("Digite o nome completo: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (Rua, nº, bairro, cidade/UF): ")
        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        clientes.append(cliente)
        print("Cliente cadastrado com sucesso!")

#FUNÇÃO PARA FILTRAR USUÁRIOS JÁ CADASTRADOS NO SISTEMA
def filtro_cliente(cpf, clientes):
    filtro = [cliente for cliente in clientes if cliente.cpf==cpf]
    return filtro[0] if filtro else None
      
#FUNÇÃO PARA CRIAR CONTA
def criar_conta(numero_conta, clientes, contas):
    cpf = (input("Digite o CPF (somente números): "))
    filtro = filtro_cliente(cpf, clientes)
    if filtro:
        print("Conta Criada com sucesso!")
        conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=filtro)
        contas.append(conta)
        filtro.contas.append(conta)
    else:
        print("Usuário não cadastro, não é possível criar a conta!")

#FUNÇÃO PARA LISTAR CONTAS CADASTRADAS
def listar_contas(contas):
    for conta in contas:
        print(f'{conta}')

#FUNÇÃO PARA DEPOSITAR
def deposito(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtro_cliente(cpf, clientes)
    if cliente:
        valor_deposito = float(input("Digite o valor para depósito: "))
        while valor_deposito <= 0:
            valor_deposito = float(input("Valor inválido. Digite um valor válido para depósito: "))
        transacao = Deposito(valor_deposito)
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return
        cliente.realizar_transacao(conta, transacao)
    else:
        print("Cliente não encontrado!")

#RECUPERAR CONTA DO CLIENTE
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não tem contas cadastradas!")
    else:
        return cliente.contas[0]

#FUNÇÃO PARA SAQUE
def saque(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtro_cliente(cpf, clientes)
    if cliente:
        valor_saque = float(input("Digite o valor para saque: "))
        transacao = Saque(valor_saque)
        conta = recuperar_conta_cliente(cliente)
    else:
        print("Cliente não encontrado!")
    if conta:
        cliente.realizar_transacao(conta, transacao)
    else:
        return

#FUNÇÃO PARA VISUALIZAR O EXTRATO
def extrato(clientes):
    mensagem = "Aqui está o seu extrato bancário"
    print(mensagem.upper().center(len(mensagem) + 8, "-"))
    
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtro_cliente(cpf, clientes)

    if cliente:
        conta = recuperar_conta_cliente(cliente)
    else:
        print("Cliente não encontrado!")
        return  
    if conta:
        transacoes = conta.historico.transacoes
        if transacoes:
            for transacao in transacoes:
                print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f}")
            print(f"Saldo: {conta.saldo:.2f}")
    else:
        return  

def run():
    clientes = []
    contas = []

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
        #CRIAR CLIENTE
        elif escolha == 0:
            criar_cliente(clientes)
        #CRIAR CONTA
        elif escolha == 1:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        #SAQUE
        elif escolha == 2:
            saque(clientes)
        #DEPÓSITOS
        elif escolha == 3:
            deposito(clientes)
        #EXTRATOS
        elif escolha == 4:
            extrato(clientes)
        #LISTAR CONTAS
        elif escolha == 5:
            listar_contas(contas)
        #SAÍDA DO SISTEMA
        elif escolha == 6:
            print("Obrigado por utilizar o Banco V1! Volte Sempre!")
            break

run()
