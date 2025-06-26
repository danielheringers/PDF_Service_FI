# Use uma imagem base para instalar o UV e as dependências
FROM python:3.12.4-alpine as builder

# Definir variáveis de ambiente para o builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências necessárias para o UV e criar o diretório de trabalho
RUN apk add --no-cache \
    curl \
    bash \
    libc6-compat \
    libffi-dev \
    openssl-dev \
    gcc \
    musl-dev \
    make \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV LANG=pt_BR.UTF-8  
ENV LANGUAGE=pt_BR:pt  
ENV LC_ALL=pt_BR.UTF-8

WORKDIR /app

# Copiar arquivos necessários para instalar o UV
COPY pyproject.toml .
COPY uv.lock .

# Instalar o UV
RUN uv init . \
    && uv self update \
    && uv sync

# Etapa final para criar a imagem leve
FROM python:3.12.4-alpine

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG=pt_BR.UTF-8  
ENV LANGUAGE=pt_BR:pt  
ENV LC_ALL=pt_BR.UTF-8

# Instalar dependências necessárias para o runtime
RUN apk add --no-cache \
    libffi \
    openssl \
    curl

# Copiar os arquivos do builder para a imagem final
COPY --from=builder /app /app

# Definir o diretório de trabalho
WORKDIR /app

# Expor a porta do servidor
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
