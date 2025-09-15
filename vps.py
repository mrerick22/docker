import os
import subprocess
import random
import string

# Porta inicial para mapeamento SSH
PORT_INICIAL = 2222

# Diretório para armazenar informações de VPS
DB_FILE = "vps_db.txt"

def gerar_senha(tamanho=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

def salvar_vps(nome, usuario, senha, porta):
    with open(DB_FILE, "a") as f:
        f.write(f"{nome},{usuario},{senha},{porta}\n")

def carregar_vpss():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        linhas = f.readlines()
    vpss = [linha.strip().split(",") for linha in linhas]
    return vpss

def criar_vps(nome):
    usuario = f"user_{random.randint(1000,9999)}"
    senha = gerar_senha()
    porta = PORT_INICIAL + len(carregar_vpss())
    imagem = f"vps_{nome.lower()}"
    
    # Build do container
    subprocess.run(f"docker build --build-arg USERNAME={usuario} --build-arg PASSWORD={senha} -t {imagem} .", shell=True)
    
    # Rodar container
    subprocess.run(f"docker run -d --name {nome} -p {porta}:22 {imagem}", shell=True)
    
    salvar_vps(nome, usuario, senha, porta)
    print(f"[✔] VPS '{nome}' criada! SSH: ssh {usuario}@localhost -p {porta}")

def listar_vps():
    vpss = carregar_vpss()
    if not vpss:
        print("Nenhuma VPS criada ainda.")
        return
    for vps in vpss:
        nome, usuario, senha, porta = vps
        print(f"{nome}: {usuario}/{senha} -> Porta {porta}")

def parar_vps(nome):
    subprocess.run(f"docker stop {nome}", shell=True)
    print(f"[✖] VPS '{nome}' parada.")

def iniciar_vps(nome):
    subprocess.run(f"docker start {nome}", shell=True)
    print(f"[✔] VPS '{nome}' iniciada.")

def deletar_vps(nome):
    subprocess.run(f"docker rm -f {nome}", shell=True)
    # Atualiza DB
    vpss = [vps for vps in carregar_vpss() if vps[0] != nome]
    with open(DB_FILE, "w") as f:
        for vps in vpss:
            f.write(",".join(vps) + "\n")
    print(f"[🗑️] VPS '{nome}' deletada.")

# Exemplo de menu simples
def menu():
    while True:
        print("\n=== Gerenciador de VPS ===")
        print("1. Criar VPS")
        print("2. Listar VPSs")
        print("3. Parar VPS")
        print("4. Iniciar VPS")
        print("5. Deletar VPS")
        print("6. Sair")
        escolha = input("Escolha: ")
        if escolha == "1":
            nome = input("Nome da VPS: ")
            criar_vps(nome)
        elif escolha == "2":
            listar_vps()
        elif escolha == "3":
            nome = input("Nome da VPS: ")
            parar_vps(nome)
        elif escolha == "4":
            nome = input("Nome da VPS: ")
            iniciar_vps(nome)
        elif escolha == "5":
            nome = input("Nome da VPS: ")
            deletar_vps(nome)
        elif escolha == "6":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
