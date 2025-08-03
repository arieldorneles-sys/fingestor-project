import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Navigate } from 'react-router-dom';
import { Eye, EyeOff, LogIn, User } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('admin@empresaexemplo.com.br');
  const [password, setPassword] = useState('admin123');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login, isAuthenticated } = useAuth();

  // Se já estiver autenticado, redireciona para o dashboard
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await login(email, password);
      if (!result.success) {
        setError(result.error || 'Erro ao fazer login. Verifique suas credenciais.');
      }
    } catch (err) {
      console.error('Erro de login:', err);
      setError('Erro de conexão. Verifique se o servidor está rodando na porta 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    setEmail('admin@empresaexemplo.com.br');
    setPassword('admin123');
    setError('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="max-w-md w-full space-y-8 fade-in">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-primary rounded-full flex items-center justify-center mb-4 shadow-lg">
            <User className="h-8 w-8 text-primary-foreground" />
          </div>
          <h2 className="text-3xl font-bold text-foreground">FinGestor</h2>
          <p className="mt-2 text-muted-foreground">
            Sistema ERP Financeiro
          </p>
        </div>

        {/* Formulário */}
        <div className="bg-card p-8 rounded-lg border border-border shadow-xl">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 bg-input border border-border rounded-md text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                placeholder="Digite seu email"
              />
            </div>

            {/* Senha */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
                Senha
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 pr-10 bg-input border border-border rounded-md text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                  placeholder="Digite sua senha"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center hover:text-primary transition-colors"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4 text-muted-foreground" />
                  ) : (
                    <Eye className="h-4 w-4 text-muted-foreground" />
                  )}
                </button>
              </div>
            </div>

            {/* Erro */}
            {error && (
              <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-md text-sm">
                ⚠️ {error}
              </div>
            )}

            {/* Botão de Login */}
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center px-4 py-3 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-foreground"></div>
              ) : (
                <>
                  <LogIn className="h-4 w-4 mr-2" />
                  Entrar no Sistema
                </>
              )}
            </button>
          </form>

          {/* Credenciais de demonstração */}
          <div className="mt-6 pt-6 border-t border-border">
            <div className="text-center">
              <p className="text-sm text-muted-foreground mb-3">
                🎯 Credenciais já preenchidas para demonstração
              </p>
              <button
                type="button"
                onClick={handleDemoLogin}
                className="text-sm text-accent hover:text-accent/80 underline transition-colors"
              >
                Restaurar credenciais padrão
              </button>
            </div>
            <div className="mt-4 p-3 bg-muted/30 rounded-md text-xs text-muted-foreground space-y-1">
              <div className="flex items-center gap-2">
                <span>📧</span>
                <span>Email: admin@empresaexemplo.com.br</span>
              </div>
              <div className="flex items-center gap-2">
                <span>🔑</span>
                <span>Senha: admin123</span>
              </div>
            </div>
          </div>
        </div>

        {/* Instruções */}
        <div className="bg-card/50 p-4 rounded-lg border border-border/50">
          <div className="text-center text-sm text-muted-foreground">
            <p className="font-medium text-foreground mb-2">💡 Como usar:</p>
            <ol className="text-left space-y-1 max-w-xs mx-auto">
              <li>1. Certifique-se que o backend está rodando (porta 8000)</li>
              <li>2. Use as credenciais já preenchidas</li>
              <li>3. Clique em "Entrar no Sistema"</li>
            </ol>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground">
          <p>© 2025 FinGestor - Sistema ERP Financeiro</p>
          <p className="mt-1">Desenvolvido com ❤️ por Manus AI</p>
        </div>
      </div>
    </div>
  );
};

export default Login;

