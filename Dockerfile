# Dockerfile
FROM ubuntu:22.04

# Evitar perguntas durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar e instalar dependências básicas + SSH
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    curl \
    vim \
    net-tools \
    iproute2 \
    && mkdir /var/run/sshd

# Configurar usuário padrão
ARG USERNAME=vpsuser
ARG PASSWORD=vpspass

RUN useradd -m -s /bin/bash $USERNAME && \
    echo "$USERNAME:$PASSWORD" | chpasswd && \
    usermod -aG sudo $USERNAME

# Permitir login root via SSH (opcional)
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expor porta SSH
EXPOSE 22

# Start SSH
CMD ["/usr/sbin/sshd","-D"]
