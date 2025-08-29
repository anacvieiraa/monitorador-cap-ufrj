#!/bin/bash
echo "Configurando Monitorador CAP-UFRJ..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instale primeiro."
    exit 1
fi

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "Criando arquivo .env de exemplo..."
    cp .env.example .env
    echo "Edite o arquivo .env com suas credenciais Twilio!"
fi

echo "Setup completo! Ative o ambiente com: source venv/bin/activate"
