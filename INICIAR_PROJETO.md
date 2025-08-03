# 🚀 Guia de Inicialização - FinGestor

## 📋 Pré-requisitos (Instalar antes de começar)

1. **Python 3.11+**: https://python.org/downloads/
2. **Node.js 18+**: https://nodejs.org/
3. **Git**: https://git-scm.com/download/win
4. **VS Code**: https://code.visualstudio.com/

## 🎯 Passo a Passo para Iniciar

### 1. Abrir o Projeto no VS Code

1. Abra o VS Code
2. Vá em `File > Open Workspace from File...`
3. Selecione o arquivo `fingestor.code-workspace`
4. O VS Code abrirá com a estrutura correta do projeto

### 2. Instalar Extensões Recomendadas

Quando abrir o workspace, o VS Code sugerirá instalar as extensões recomendadas. Clique em **"Install All"**.

### 3. Configurar o Backend (Python)

**Terminal 1 - Backend:**
```bash
# Navegar para o backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env

# Criar dados de exemplo
python create_sample_data.py

# Executar servidor
python run_dev.py
```

### 4. Configurar o Frontend (React)

**Terminal 2 - Frontend:**
```bash
# Navegar para o frontend
cd frontend

# Instalar pnpm globalmente
npm install -g pnpm

# Instalar dependências
pnpm install

# Executar servidor de desenvolvimento
pnpm run dev
```

### 5. Acessar o Sistema

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

### 6. Login no Sistema

- **Email**: admin@empresaexemplo.com.br
- **Senha**: admin123

## 🔧 Comandos Úteis

### Backend
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar testes
pytest

# Executar com debug
python -m debugpy --listen 5678 --wait-for-client run_dev.py
```

### Frontend
```bash
# Executar em modo desenvolvimento
pnpm run dev

# Build para produção
pnpm run build

# Executar testes
pnpm test
```

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
- Certifique-se de que Python está instalado e no PATH
- Reinicie o VS Code após instalar Python

### Erro: "pnpm não encontrado"
```bash
npm install -g pnpm
```

### Erro: "Porta 8000 em uso"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erro: "Módulo não encontrado"
```bash
# Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
pnpm install
```

## 📁 Estrutura de Arquivos Importantes

```
fingestor/
├── fingestor.code-workspace    # Arquivo de workspace do VS Code
├── INICIAR_PROJETO.md         # Este arquivo
├── README.md                  # Documentação principal
├── backend/
│   ├── app/
│   │   ├── main.py           # Aplicação principal FastAPI
│   │   ├── models/           # Modelos do banco de dados
│   │   ├── routers/          # Endpoints da API
│   │   └── schemas/          # Validações Pydantic
│   ├── run_dev.py            # Script para executar o servidor
│   ├── create_sample_data.py # Script para dados de exemplo
│   └── requirements.txt      # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Componente principal React
│   │   ├── pages/           # Páginas da aplicação
│   │   └── components/      # Componentes reutilizáveis
│   └── package.json         # Dependências Node.js
└── docs/                    # Documentação completa
```

## 🎉 Próximos Passos

1. Explore o dashboard em http://localhost:3000
2. Teste as funcionalidades de clientes e fornecedores
3. Experimente a simulação de impostos
4. Consulte a documentação completa em `docs/README_COMPLETO.md`
5. Personalize o sistema conforme suas necessidades

## 📞 Suporte

Se encontrar problemas:
1. Consulte a seção "Troubleshooting" em `docs/README_COMPLETO.md`
2. Verifique se todos os pré-requisitos estão instalados
3. Certifique-se de que as portas 3000 e 8000 estão livres

**Boa sorte com seu projeto FinGestor! 🚀**

