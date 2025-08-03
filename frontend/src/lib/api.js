import axios from 'axios';

// Configuração base da API
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos de timeout
});

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('Fazendo requisição para:', config.url, config.method?.toUpperCase());
    return config;
  },
  (error) => {
    console.error('Erro na requisição:', error);
    return Promise.reject(error);
  }
);

// Interceptor para tratar respostas e erros
api.interceptors.response.use(
  (response) => {
    console.log('Resposta recebida:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('Erro na resposta:', error);
    
    if (error.response?.status === 401) {
      // Token expirado ou inválido
      console.log('Token inválido, removendo do localStorage');
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      
      // Só redireciona se não estiver na página de login
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Serviços de autenticação
export const authService = {
  login: async (email, password) => {
    console.log('authService.login chamado com:', { email });
    
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    try {
      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log('Login bem-sucedido:', response.data);
      return response.data;
    } catch (error) {
      console.error('Erro no authService.login:', error);
      throw error;
    }
  },
  
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  getMe: async () => {
    console.log('authService.getMe chamado');
    try {
      const response = await api.get('/auth/me');
      console.log('getMe bem-sucedido:', response.data);
      return response.data;
    } catch (error) {
      console.error('Erro no authService.getMe:', error);
      throw error;
    }
  },
  
  refreshToken: async () => {
    const response = await api.post('/auth/refresh');
    return response.data;
  },
};

// Serviços de clientes
export const customerService = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await api.get(`/customers/?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  
  getById: async (id) => {
    const response = await api.get(`/customers/${id}`);
    return response.data;
  },
  
  create: async (customerData) => {
    const response = await api.post('/customers/', customerData);
    return response.data;
  },
  
  update: async (id, customerData) => {
    const response = await api.put(`/customers/${id}`, customerData);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/customers/${id}`);
    return response.data;
  },
};

// Serviços de fornecedores
export const supplierService = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await api.get(`/suppliers/?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  
  getById: async (id) => {
    const response = await api.get(`/suppliers/${id}`);
    return response.data;
  },
  
  create: async (supplierData) => {
    const response = await api.post('/suppliers/', supplierData);
    return response.data;
  },
  
  update: async (id, supplierData) => {
    const response = await api.put(`/suppliers/${id}`, supplierData);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/suppliers/${id}`);
    return response.data;
  },
};

// Serviços financeiros
export const financialService = {
  // Contas
  getAccounts: async () => {
    const response = await api.get('/financial/accounts/');
    return response.data;
  },
  
  createAccount: async (accountData) => {
    const response = await api.post('/financial/accounts/', accountData);
    return response.data;
  },
  
  updateAccount: async (id, accountData) => {
    const response = await api.put(`/financial/accounts/${id}`, accountData);
    return response.data;
  },
  
  deleteAccount: async (id) => {
    const response = await api.delete(`/financial/accounts/${id}`);
    return response.data;
  },
  
  // Transações
  getTransactions: async (skip = 0, limit = 100) => {
    const response = await api.get(`/financial/transactions/?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  
  createTransaction: async (transactionData) => {
    const response = await api.post('/financial/transactions/', transactionData);
    return response.data;
  },
  
  updateTransaction: async (id, transactionData) => {
    const response = await api.put(`/financial/transactions/${id}`, transactionData);
    return response.data;
  },
  
  deleteTransaction: async (id) => {
    const response = await api.delete(`/financial/transactions/${id}`);
    return response.data;
  },
  
  payTransaction: async (id) => {
    const response = await api.post(`/financial/transactions/${id}/pay`);
    return response.data;
  },
  
  // Categorias
  getCategories: async () => {
    const response = await api.get('/financial/categories/');
    return response.data;
  },
  
  createCategory: async (categoryData) => {
    const response = await api.post('/financial/categories/', categoryData);
    return response.data;
  },
  
  // Centros de custo
  getCostCenters: async () => {
    const response = await api.get('/financial/cost_centers/');
    return response.data;
  },
  
  createCostCenter: async (costCenterData) => {
    const response = await api.post('/financial/cost_centers/', costCenterData);
    return response.data;
  },
  
  // Simulação de impostos
  simulateTaxes: async (simulationData) => {
    const response = await api.post('/financial/taxes/simulate', simulationData);
    return response.data;
  },
  
  getTaxSimulations: async (skip = 0, limit = 100) => {
    const response = await api.get(`/financial/taxes/simulations/?skip=${skip}&limit=${limit}`);
    return response.data;
  },
};

// Serviços do dashboard
export const dashboardService = {
  getKPIs: async () => {
    const response = await api.get('/dashboard/kpis');
    return response.data;
  },
};

export default api;

