#!/bin/bash

# Nome da VPS
read -p "Nome da VPS: " NOME

# Usuário e senha da VPS
read -p "Usuário: " USUARIO
read -p "Senha: " SENHA

# Porta SSH para mapear
read -p "Porta SSH (ex: 2222): " PORTA

# Criar imagem Docker
docker build --build-arg USERNAME=$USUARIO --build-arg PASSWORD=$SENHA -t $NOME .

# Rodar container
docker run -d --name $NOME -p $PORTA:22 $NOME

echo "VPS '$NOME' criada! Conecte via SSH: ssh $USUARIO@localhost -p $PORTA"
