#!/bin/bash

# Script de setup para desenvolvimento do FinGestor
echo "🚀 Configurando ambiente de desenvolvimento do FinGestor..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 18 ou superior."
    exit 1
fi

# Configurar backend
echo "📦 Configurando backend..."
cd backend

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "🔧 Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências do backend..."
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
fi

# Voltar para o diretório raiz
cd ..

# Configurar frontend
echo "📦 Configurando frontend..."
cd frontend

# Verificar se pnpm está instalado
if ! command -v pnpm &> /dev/null; then
    echo "🔧 Instalando pnpm..."
    npm install -g pnpm
fi

# Instalar dependências
echo "📥 Instalando dependências do frontend..."
pnpm install

# Voltar para o diretório raiz
cd ..

echo "✅ Setup concluído!"
echo ""
echo "📋 Para executar o projeto:"
echo "   Backend:  cd backend && source venv/bin/activate && python run_dev.py"
echo "   Frontend: cd frontend && pnpm run dev"
echo ""
echo "🌐 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

