# imagem base com dependências de build
FROM python:3.12-slim AS base

# Variáveis de ambiente para Poetry
ENV POETRY_VERSION=1.8.5 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Instalando dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libffi-dev libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalando o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION && \
    ln -s $HOME/.local/bin/poetry /usr/local/bin/poetry

# Criando diretório de trabalho
WORKDIR /app

# Copiando arquivos de dependência
COPY pyproject.toml poetry.lock* /app/

# Instalando dependências
RUN poetry install --no-root

# Copiando o restante do código
COPY . /app

# Expondo porta padrão do Uvicorn
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
