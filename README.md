# 📄 PyPDF Server

## 📌 Sobre o Projeto

Esta API recebe arquivos PDF contendo dados estruturados e os converte em DataFrames para posterior processamento por IA (Gemini). O desafio é que os PDFs podem variar conforme a empresa, exigindo um módulo específico para cada formato.

## 📂 Estrutura do Projeto

```
app/
├── config/         # Arquivos de configuração de ambiente
├── controller/     # Contém a lógica para manipulação de arquivos PDF
├── gemini/         # Integração com o Gemini
├── manager/        # Contém arquivos de gerenciamento
├── modules/        # Módulos específicos para cada formato de PDF
├── pdf/            # Pasta onde os PDFs enviados pelo frontend são armazenados
├── routers/        # Gerencia as rotas da API
├── test/           # Testes unitários da API
├── upload/         # Armazena temporariamente os arquivos convertidos para envio ao Gemini
├── utils/          # Funções auxiliares, como extração de texto
main.py             # Arquivo principal da API
```

## 🔄 Fluxo da API

1. O frontend faz o upload de um arquivo PDF via endpoint da API.
2. O arquivo é salvo temporariamente na pasta `pdf/`.
3. O sistema identifica o tipo de documento (baseado na empresa informada no upload).
4. A API busca o módulo correto dentro de `modules/` (exemplo: `modules/boticario.py`).
5. O PDF é processado e convertido em um DataFrame.
6. O DataFrame é salvo em `upload/` como um arquivo TXT para envio ao Gemini.
7. O PDF original é removido da pasta `pdf/`.
8. O frontend recebe a resposta com os dados processados.

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework para construção da API
- **PyMuPDF (fitz)** - Extração de texto de PDFs
- **Pandas** - Manipulação e conversão de dados
- **Google-Genai** - Integração com Gemini

## ⚙️ Pré-requisitos

Antes de rodar o projeto, é necessário instalar e configurar o **Pyenv** e o **Poetry**.

### Instalando o Pyenv no WSL

Se ainda não tem o Pyenv instalado, siga os passos abaixo:

```bash
sudo apt install -y \
    make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev libncursesw5-dev xz-utils tk-dev \
    libffi-dev liblzma-dev python3-openssl git
```

```bash
curl -fsSL https://pyenv.run | bash
```

Após a instalação, adicione as seguintes linhas ao seu `~/.bashrc` ou `~/.zshrc`:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
```

Reinicie o terminal e instale a versão do Python desejada:

```bash
pyenv install
```

### Instalando o Poetry

O projeto utiliza o **Poetry** na versão **1.8.5** para gerenciar dependências. Instale com:

```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.8.5
```

Após a instalação, adicione o Poetry ao PATH (se necessário):

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

```bash
poetry completions bash >> ~/.bash_completion
```

Verifique a versão instalada:

```bash
poetry --version
```

## 🛠 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/guild-zero-one/pypdf-server.git
   cd pypdf-server
   ```
2. Instale as dependências com Poetry:
   ```bash
   poetry install
   ```
3. Ative o ambiente virtual do Poetry:
   ```bash
   poetry shell
   ```
4. Execute a API:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Acesse a documentação interativa:
   ```
   http://127.0.0.1:8000/docs
   ```
