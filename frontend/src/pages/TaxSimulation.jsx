import { useState, useEffect } from 'react';
import { financialService } from '../lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import {
  Calculator,
  TrendingUp,
  DollarSign,
  FileText,
  AlertCircle,
  Info
} from 'lucide-react';

const TaxSimulation = () => {
  const [formData, setFormData] = useState({
    revenue: '',
    tax_regime: ''
  });
  const [simulation, setSimulation] = useState(null);
  const [simulations, setSimulations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadSimulations();
  }, []);

  const loadSimulations = async () => {
    try {
      const data = await financialService.getTaxSimulations();
      setSimulations(data);
    } catch (err) {
      console.error('Erro ao carregar simulações:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const simulationData = {
        revenue: parseFloat(formData.revenue),
        tax_regime: formData.tax_regime
      };

      const result = await financialService.simulateTaxes(simulationData);
      setSimulation(result);
      loadSimulations(); // Recarregar lista de simulações
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao simular impostos');
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
    return `${value.toFixed(2)}%`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Simulação de Impostos</h1>
        <Calculator className="h-8 w-8 text-blue-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Formulário de Simulação */}
        <Card>
          <CardHeader>
            <CardTitle>Nova Simulação</CardTitle>
            <CardDescription>
              Simule os impostos para diferentes regimes tributários
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="revenue">Receita Bruta Anual (R$) *</Label>
                <Input
                  id="revenue"
                  type="number"
                  step="0.01"
                  value={formData.revenue}
                  onChange={(e) => setFormData({...formData, revenue: e.target.value})}
                  placeholder="1000000.00"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="tax_regime">Regime Tributário *</Label>
                <Select
                  value={formData.tax_regime}
                  onValueChange={(value) => setFormData({...formData, tax_regime: value})}
                  required
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o regime tributário" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="simples_nacional">Simples Nacional</SelectItem>
                    <SelectItem value="lucro_presumido">Lucro Presumido</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? 'Simulando...' : 'Simular Impostos'}
              </Button>
            </form>

            {/* Informações sobre os regimes */}
            <div className="mt-6 space-y-4">
              <Alert>
                <Info className="h-4 w-4" />
                <AlertDescription>
                  <strong>Simples Nacional:</strong> Regime simplificado para empresas com receita bruta anual até R$ 4,8 milhões.
                </AlertDescription>
              </Alert>
              
              <Alert>
                <Info className="h-4 w-4" />
                <AlertDescription>
                  <strong>Lucro Presumido:</strong> Regime para empresas com receita bruta anual até R$ 78 milhões, com presunção de lucro.
                </AlertDescription>
              </Alert>
            </div>
          </CardContent>
        </Card>

        {/* Resultado da Simulação */}
        {simulation && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="mr-2 h-5 w-5" />
                Resultado da Simulação
              </CardTitle>
              <CardDescription>
                <Badge variant="outline">
                  {simulation.simulated_taxes.regime}
                </Badge>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">Receita Anual</Label>
                  <div className="text-lg font-semibold">
                    {formatCurrency(simulation.simulated_taxes.annual_revenue)}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">Total de Impostos</Label>
                  <div className="text-lg font-semibold text-red-600">
                    {formatCurrency(simulation.simulated_taxes.total_tax)}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">Receita Líquida</Label>
                  <div className="text-lg font-semibold text-green-600">
                    {formatCurrency(simulation.simulated_taxes.net_income)}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">Impostos Mensais</Label>
                  <div className="text-lg font-semibold">
                    {formatCurrency(simulation.simulated_taxes.monthly_tax)}
                  </div>
                </div>
              </div>

              {simulation.simulated_taxes.tax_rate && (
                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">Alíquota Efetiva</Label>
                  <div className="text-lg font-semibold">
                    {formatPercentage(simulation.simulated_taxes.tax_rate)}
                  </div>
                </div>
              )}

              {/* Detalhamento dos impostos */}
              <div className="space-y-2">
                <Label className="text-sm text-gray-600">Detalhamento</Label>
                <div className="space-y-1">
                  {Object.entries(simulation.simulated_taxes.breakdown).map(([tax, value]) => (
                    <div key={tax} className="flex justify-between text-sm">
                      <span className="capitalize">{tax.replace('_', ' ')}</span>
                      <span>{formatCurrency(value)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Histórico de Simulações */}
      {simulations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="mr-2 h-5 w-5" />
              Histórico de Simulações
            </CardTitle>
            <CardDescription>
              Suas simulações anteriores
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {simulations.slice(0, 5).map((sim) => (
                <div key={sim.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">
                        {sim.simulated_taxes.regime}
                      </Badge>
                      <span className="text-sm text-gray-500">
                        {new Date(sim.created_at).toLocaleDateString('pt-BR')}
                      </span>
                    </div>
                    <div className="text-sm">
                      Receita: {formatCurrency(sim.simulated_taxes.annual_revenue)}
                    </div>
                  </div>
                  <div className="text-right space-y-1">
                    <div className="font-semibold text-red-600">
                      {formatCurrency(sim.simulated_taxes.total_tax)}
                    </div>
                    <div className="text-sm text-gray-500">
                      impostos/ano
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default TaxSimulation;

