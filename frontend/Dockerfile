FROM node:20-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Instalar pnpm globalmente
RUN npm install -g pnpm

# Instalar dependências
RUN pnpm install

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 3000

# Comando padrão para desenvolvimento
CMD ["pnpm", "run", "dev", "--", "--host"]

