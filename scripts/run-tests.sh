#!/bin/bash

# Script para executar testes do FinGestor
echo "🧪 Executando testes do FinGestor..."

# Ir para o diretório do backend
cd backend

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Execute primeiro: ./scripts/dev-setup.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Executar testes
echo "🧪 Executando testes do backend..."
python -m pytest tests/ -v

# Verificar se os testes passaram
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
else
    echo "❌ Alguns testes falharam."
    exit 1
fi

echo "🎉 Testes concluídos com sucesso!"

