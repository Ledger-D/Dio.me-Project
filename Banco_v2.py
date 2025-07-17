import textwrap

def menu():
    """Exibe o menu de opções para o usuário e retorna a escolha."""
    menu_texto = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta.

    Args:
        saldo (float): Saldo atual da conta.
        valor (float): Valor a ser depositado.
        extrato (str): Histórico de transações.

    Returns:
        tuple: (saldo atualizado, extrato atualizado).
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, limite_saques, numero_saques):
    """
    Realiza um saque na conta.

    Args:
        saldo (float): Saldo atual da conta.
        valor (float): Valor a ser sacado.
        extrato (str): Histórico de transações.
        limite (float): Limite máximo por saque.
        limite_saques (int): Número máximo de saques permitidos.
        numero_saques (int): Contador de saques realizados.

    Returns:
        tuple: (saldo atualizado, extrato atualizado, número de saques atualizado).
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}. @@@")
    elif excedeu_saques:
        print(f"\n@@@ Operação falhou! Número máximo de {limite_saques} saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.

    Args:
        saldo (float): Saldo atual da conta.
        extrato (str): Histórico de transações.
    """
    print("\n=============== EXTRATO ===============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("=======================================")

def criar_usuario(usuarios):
    """
    Cria um novo usuário.

    Args:
        usuarios (list): Lista de usuários cadastrados.

    Returns:
        list: Lista de usuários atualizada.
    """
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return usuarios

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")
    return usuarios

def filtrar_usuario(cpf, usuarios):
    """
    Filtra um usuário pelo CPF.

    Args:
        cpf (str): CPF a ser filtrado.
        usuarios (list): Lista de usuários cadastrados.

    Returns:
        dict or None: O usuário encontrado ou None se não for encontrado.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    """
    Cria uma nova conta bancária para um usuário existente.

    Args:
        agencia (str): Número da agência.
        numero_conta (int): Número da próxima conta disponível.
        usuarios (list): Lista de usuários cadastrados.

    Returns:
        dict or None: A nova conta criada ou None se o usuário não for encontrado.
    """
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

def listar_contas(contas):
    """
    Lista todas as contas cadastradas.

    Args:
        contas (list): Lista de contas cadastradas.
    """
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    """Função principal que executa o programa bancário."""
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                limite_saques=LIMITE_SAQUES,
                numero_saques=numero_saques,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            usuarios = criar_usuario(usuarios)

        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()def