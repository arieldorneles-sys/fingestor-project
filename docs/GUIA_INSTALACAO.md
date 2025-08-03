# Guia de Instalação - FinGestor

## Instalação Rápida (Windows 11)

### Pré-requisitos

1. **Python 3.11+**: Baixe em [python.org](https://python.org)
2. **Node.js 18+**: Baixe em [nodejs.org](https://nodejs.org)
3. **Git**: Baixe em [git-scm.com](https://git-scm.com)
4. **VS Code**: Baixe em [code.visualstudio.com](https://code.visualstudio.com)

### Passo a Passo

1. **Clone o repositório**:
```bash
git clone https://github.com/seu-usuario/fingestor.git
cd fingestor
```

2. **Configure o Backend**:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

3. **Configure o Frontend**:
```bash
cd ..\frontend
npm install -g pnpm
pnpm install
```

4. **Execute o sistema**:

**Terminal 1 (Backend)**:
```bash
cd backend
venv\Scripts\activate
python run_dev.py
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
pnpm run dev
```

5. **Acesse o sistema**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Credenciais Padrão

- **Email**: admin@empresaexemplo.com.br
- **Senha**: admin123

### Populando com Dados de Exemplo

```bash
cd backend
venv\Scripts\activate
python create_sample_data.py
```

## Solução de Problemas

### Erro de Porta em Uso
```bash
# Matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problemas com Python
```bash
# Reinstalar ambiente virtual
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Problemas com Node.js
```bash
# Limpar cache e reinstalar
pnpm store prune
rmdir /s node_modules
pnpm install
```

## Próximos Passos

1. Altere a senha padrão
2. Configure dados da sua empresa
3. Cadastre seus clientes e fornecedores
4. Explore as funcionalidades do sistema

Para documentação completa, consulte `docs/README_COMPLETO.md`.

