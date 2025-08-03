import { useState, useEffect } from 'react';
import { dashboardService } from '../lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  FileText,
  CreditCard,
  Building2,
  AlertCircle
} from 'lucide-react';

const Dashboard = () => {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadKPIs();
  }, []);

  const loadKPIs = async () => {
    try {
      const data = await dashboardService.getKPIs();
      setKpis(data);
    } catch (err) {
      setError('Erro ao carregar dados do dashboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatPercentage = (value) => {
    return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
  };

  const getVariationColor = (variation) => {
    if (variation > 0) return 'text-green-600';
    if (variation < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  const getVariationIcon = (variation) => {
    if (variation > 0) return <TrendingUp className="h-4 w-4" />;
    if (variation < 0) return <TrendingDown className="h-4 w-4" />;
    return null;
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <Card className="border-red-200 bg-red-50">
          <CardContent className="p-6">
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
              <span className="text-red-800">{error}</span>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <Badge variant="outline">
          {kpis?.period?.current_month}
        </Badge>
      </div>

      {/* KPIs Financeiros */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Receitas</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(kpis?.financial_kpis?.revenue?.current || 0)}
            </div>
            <div className={`flex items-center text-xs ${getVariationColor(kpis?.financial_kpis?.revenue?.variation || 0)}`}>
              {getVariationIcon(kpis?.financial_kpis?.revenue?.variation || 0)}
              <span className="ml-1">
                {formatPercentage(kpis?.financial_kpis?.revenue?.variation || 0)} vs mês anterior
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Despesas</CardTitle>
            <TrendingDown className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(kpis?.financial_kpis?.expenses?.current || 0)}
            </div>
            <div className={`flex items-center text-xs ${getVariationColor(kpis?.financial_kpis?.expenses?.variation || 0)}`}>
              {getVariationIcon(kpis?.financial_kpis?.expenses?.variation || 0)}
              <span className="ml-1">
                {formatPercentage(kpis?.financial_kpis?.expenses?.variation || 0)} vs mês anterior
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Lucro Líquido</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(kpis?.financial_kpis?.profit?.current || 0)}
            </div>
            <div className={`flex items-center text-xs ${getVariationColor(kpis?.financial_kpis?.profit?.variation || 0)}`}>
              {getVariationIcon(kpis?.financial_kpis?.profit?.variation || 0)}
              <span className="ml-1">
                {formatPercentage(kpis?.financial_kpis?.profit?.variation || 0)} vs mês anterior
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Margem Líquida</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatPercentage(kpis?.financial_kpis?.margin?.current || 0)}
            </div>
            <div className={`flex items-center text-xs ${getVariationColor(kpis?.financial_kpis?.margin?.variation || 0)}`}>
              {getVariationIcon(kpis?.financial_kpis?.margin?.variation || 0)}
              <span className="ml-1">
                {formatPercentage(kpis?.financial_kpis?.margin?.variation || 0)} vs mês anterior
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Contas a Pagar/Receber */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Contas a Receber</CardTitle>
            <CardDescription>Valores pendentes de recebimento</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {formatCurrency(kpis?.financial_kpis?.accounts_receivable || 0)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Contas a Pagar</CardTitle>
            <CardDescription>Valores pendentes de pagamento</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {formatCurrency(kpis?.financial_kpis?.accounts_payable || 0)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Fluxo de Caixa Projetado</CardTitle>
            <CardDescription>Próximos 30 dias</CardDescription>
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${
              (kpis?.financial_kpis?.projected_cash_flow || 0) >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {formatCurrency(kpis?.financial_kpis?.projected_cash_flow || 0)}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Contadores */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Clientes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{kpis?.counters?.customers || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Fornecedores</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{kpis?.counters?.suppliers || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Notas Fiscais</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{kpis?.counters?.invoices || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Boletos</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{kpis?.counters?.billings || 0}</div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;

