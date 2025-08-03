import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Suppliers from './pages/Suppliers';
import TaxSimulation from './pages/TaxSimulation';
import './App.css';

// Componente para proteger rotas
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Componente para redirecionar usuários autenticados
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return !isAuthenticated ? children : <Navigate to="/dashboard" />;
};

function App() {
  // Força o tema dark sempre
  React.useEffect(() => {
    document.documentElement.classList.add('dark');
    document.body.classList.add('dark');
  }, []);

  return (
    <div className="dark min-h-screen bg-background text-foreground">
      <AuthProvider>
        <Router>
          <Routes>
            {/* Rotas públicas */}
            <Route path="/login" element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } />
            
            {/* Rotas protegidas */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            } />
            
            <Route path="/customers" element={
              <ProtectedRoute>
                <Layout>
                  <Customers />
                </Layout>
              </ProtectedRoute>
            } />
            
            <Route path="/suppliers" element={
              <ProtectedRoute>
                <Layout>
                  <Suppliers />
                </Layout>
              </ProtectedRoute>
            } />
            
            <Route path="/tax-simulation" element={
              <ProtectedRoute>
                <Layout>
                  <TaxSimulation />
                </Layout>
              </ProtectedRoute>
            } />
            
            {/* Páginas em desenvolvimento */}
            <Route path="/financial" element={
              <ProtectedRoute>
                <Layout>
                  <div className="text-center py-12">
                    <h2 className="text-2xl font-bold text-foreground mb-4">Financeiro</h2>
                    <p className="text-muted-foreground">Esta página está em desenvolvimento.</p>
                  </div>
                </Layout>
              </ProtectedRoute>
            } />
            
            <Route path="/invoices" element={
              <ProtectedRoute>
                <Layout>
                  <div className="text-center py-12">
                    <h2 className="text-2xl font-bold text-foreground mb-4">Notas Fiscais</h2>
                    <p className="text-muted-foreground">Esta página está em desenvolvimento.</p>
                  </div>
                </Layout>
              </ProtectedRoute>
            } />
            
            <Route path="/billings" element={
              <ProtectedRoute>
                <Layout>
                  <div className="text-center py-12">
                    <h2 className="text-2xl font-bold text-foreground mb-4">Boletos</h2>
                    <p className="text-muted-foreground">Esta página está em desenvolvimento.</p>
                  </div>
                </Layout>
              </ProtectedRoute>
            } />
            
            <Route path="/settings" element={
              <ProtectedRoute>
                <Layout>
                  <div className="text-center py-12">
                    <h2 className="text-2xl font-bold text-foreground mb-4">Configurações</h2>
                    <p className="text-muted-foreground">Esta página está em desenvolvimento.</p>
                  </div>
                </Layout>
              </ProtectedRoute>
            } />
            
            {/* Rota padrão */}
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;

