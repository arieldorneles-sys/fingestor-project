# FinGestor - Sistema ERP Financeiro

![FinGestor Logo](https://via.placeholder.com/200x80/2563eb/ffffff?text=FinGestor)

**Sistema ERP financeiro completo para pequenas e médias empresas brasileiras**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Visão Geral

O FinGestor é uma solução SaaS moderna e escalável para gestão completa de pequenas empresas, com foco em finanças, vendas, emissão de notas fiscais e controle de fluxo de caixa. Desenvolvido com tecnologias atuais e pensado especificamente para o mercado brasileiro.

### ✨ Principais Funcionalidades

- 📊 **Dashboard Executivo** com KPIs financeiros em tempo real
- 👥 **Gestão de Clientes e Fornecedores** com validação automática de documentos
- 💰 **Módulo Financeiro Completo** com contas a pagar/receber e conciliação bancária
- 🧮 **Simulação de Impostos** para Simples Nacional e Lucro Presumido
- 📱 **Interface Responsiva** otimizada para desktop e mobile
- 🔐 **Autenticação Segura** com JWT e controle de acesso
- 🐳 **Containerizado** com Docker para fácil deploy

## 🛠️ Tecnologias

### Backend
- **Python 3.11+** com FastAPI
- **SQLAlchemy** para ORM
- **PostgreSQL** (produção) / SQLite (desenvolvimento)
- **JWT** para autenticação
- **Pydantic** para validação de dados

### Frontend
- **React 18** com TypeScript
- **TailwindCSS** para estilização
- **shadcn/ui** para componentes
- **React Router** para navegação
- **Axios** para requisições HTTP

### DevOps
- **Docker** e Docker Compose
- **Pytest** para testes automatizados
- **GitHub Actions** para CI/CD (planejado)

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### Usando o Script Automático (Recomendado)

```bash
git clone https://github.com/seu-usuario/fingestor.git
cd fingestor
./scripts/dev-setup.sh
```

### Instalação Manual

1. **Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

2. **Frontend**:
```bash
cd frontend
npm install -g pnpm
pnpm install
```

3. **Executar**:
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python run_dev.py

# Terminal 2 - Frontend  
cd frontend && pnpm run dev
```

4. **Acessar**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs

### Credenciais Padrão
- **Email**: admin@empresaexemplo.com.br
- **Senha**: admin123

## 📖 Documentação

- [📋 Guia de Instalação Completo](docs/GUIA_INSTALACAO.md)
- [📚 Documentação Completa](docs/README_COMPLETO.md)
- [🧪 Executar Testes](scripts/run-tests.sh)

## 🐳 Docker

### Desenvolvimento
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Produção
```bash
docker-compose up -d
```

## 🧪 Testes

```bash
# Backend
cd backend
source venv/bin/activate
pytest

# Ou usar o script
./scripts/run-tests.sh
```

## 📊 Funcionalidades Detalhadas

### Dashboard Financeiro
- KPIs em tempo real (receitas, despesas, lucro, margem)
- Gráficos interativos
- Projeção de fluxo de caixa
- Alertas de vencimento

### Gestão de Clientes/Fornecedores
- Cadastro completo com validação de CPF/CNPJ
- Consulta automática de dados via ReceitaWS
- Histórico de transações
- Categorização e segmentação

### Módulo Financeiro
- Contas a pagar e receber
- Conciliação bancária (manual e automática)
- Categorias e centros de custo
- Relatórios financeiros

### Simulação de Impostos
- Cálculo automático para Simples Nacional
- Simulação de Lucro Presumido
- Comparativo entre regimes
- Histórico de simulações

## 🗺️ Roadmap

### Versão 1.1 (Q2 2025)
- [ ] Emissão de NF-e e NFS-e
- [ ] App mobile (React Native)
- [ ] Relatórios avançados

### Versão 1.2 (Q3 2025)
- [ ] Integração Open Banking
- [ ] Módulo de vendas
- [ ] Cobrança automatizada

### Versão 2.0 (Q1 2026)
- [ ] Inteligência Artificial
- [ ] Marketplace de integrações
- [ ] Multi-empresa

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Manus AI** - Sistema desenvolvido com inteligência artificial

## 📞 Suporte

- 📧 Email: suporte@fingestor.com
- 📱 WhatsApp: (11) 99999-9999
- 🌐 Website: https://fingestor.com

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**

