import { useState, useEffect, createContext, useContext } from 'react';
import { authService } from '../lib/api';

// Contexto de autenticação
const AuthContext = createContext();

// Provider de autenticação
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Verificar se há token salvo ao inicializar
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        setIsAuthenticated(true);
        
        // Verificar se o token ainda é válido
        authService.getMe()
          .then((userData) => {
            setUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));
          })
          .catch((error) => {
            console.log('Token inválido, fazendo logout:', error);
            logout();
          });
      } catch (error) {
        console.error('Erro ao carregar dados salvos:', error);
        logout();
      }
    }
    
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      console.log('Tentando fazer login com:', { email, password });
      
      const tokenData = await authService.login(email, password);
      console.log('Token recebido:', tokenData);
      
      localStorage.setItem('access_token', tokenData.access_token);
      
      // Buscar dados do usuário
      const userData = await authService.getMe();
      console.log('Dados do usuário:', userData);
      
      setUser(userData);
      setIsAuthenticated(true);
      localStorage.setItem('user', JSON.stringify(userData));
      
      return { success: true };
    } catch (error) {
      console.error('Erro no login:', error);
      
      let errorMessage = 'Erro ao fazer login';
      
      if (error.code === 'ERR_NETWORK') {
        errorMessage = 'Erro de conexão. Verifique se o backend está rodando na porta 8000.';
      } else if (error.response?.status === 401) {
        errorMessage = 'Email ou senha incorretos.';
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      
      return {
        success: false,
        error: errorMessage
      };
    }
  };

  const register = async (userData) => {
    try {
      const newUser = await authService.register(userData);
      return { success: true, user: newUser };
    } catch (error) {
      console.error('Erro no registro:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Erro ao registrar usuário'
      };
    }
  };

  const logout = () => {
    console.log('Fazendo logout...');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook para usar o contexto de autenticação
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

