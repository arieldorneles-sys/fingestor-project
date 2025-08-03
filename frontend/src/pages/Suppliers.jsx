import { useState, useEffect } from 'react';
import { supplierService } from '../lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Plus,
  Search,
  Edit,
  Trash2,
  User,
  Building,
  Phone,
  Mail,
  MapPin,
  AlertCircle
} from 'lucide-react';

const Suppliers = () => {
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    document: '',
    email: '',
    phone: '',
    address: ''
  });
  const [formLoading, setFormLoading] = useState(false);
  const [formError, setFormError] = useState('');

  useEffect(() => {
    loadSuppliers();
  }, []);

  const loadSuppliers = async () => {
    try {
      const data = await supplierService.getAll();
      setSuppliers(data);
    } catch (err) {
      setError('Erro ao carregar fornecedores');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    setFormError('');

    try {
      if (editingSupplier) {
        const updated = await supplierService.update(editingSupplier.id, formData);
        setSuppliers(suppliers.map(s => s.id === editingSupplier.id ? updated : s));
      } else {
        const newSupplier = await supplierService.create(formData);
        setSuppliers([...suppliers, newSupplier]);
      }
      
      setIsDialogOpen(false);
      resetForm();
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Erro ao salvar fornecedor');
    } finally {
      setFormLoading(false);
    }
  };

  const handleEdit = (supplier) => {
    setEditingSupplier(supplier);
    setFormData({
      name: supplier.name,
      document: supplier.document,
      email: supplier.email || '',
      phone: supplier.phone || '',
      address: supplier.address || ''
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (supplier) => {
    if (!confirm(`Tem certeza que deseja excluir o fornecedor ${supplier.name}?`)) {
      return;
    }

    try {
      await supplierService.delete(supplier.id);
      setSuppliers(suppliers.filter(s => s.id !== supplier.id));
    } catch (err) {
      alert('Erro ao excluir fornecedor');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      document: '',
      email: '',
      phone: '',
      address: ''
    });
    setEditingSupplier(null);
    setFormError('');
  };

  const formatDocument = (document) => {
    const cleaned = document.replace(/\D/g, '');
    if (cleaned.length === 11) {
      return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else if (cleaned.length === 14) {
      return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    }
    return document;
  };

  const getDocumentType = (document) => {
    const cleaned = document.replace(/\D/g, '');
    return cleaned.length === 11 ? 'CPF' : 'CNPJ';
  };

  const filteredSuppliers = suppliers.filter(supplier =>
    supplier.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    supplier.document.includes(searchTerm) ||
    (supplier.email && supplier.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-gray-900">Fornecedores</h1>
        <div className="animate-pulse">
          <div className="h-10 bg-gray-200 rounded mb-4"></div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Fornecedores</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="mr-2 h-4 w-4" />
              Novo Fornecedor
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>
                {editingSupplier ? 'Editar Fornecedor' : 'Novo Fornecedor'}
              </DialogTitle>
              <DialogDescription>
                {editingSupplier 
                  ? 'Edite as informações do fornecedor abaixo.'
                  : 'Preencha as informações do novo fornecedor abaixo.'
                }
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              {formError && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{formError}</AlertDescription>
                </Alert>
              )}
              
              <div className="space-y-2">
                <Label htmlFor="name">Nome/Razão Social *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  placeholder="Nome do fornecedor"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="document">CPF/CNPJ *</Label>
                <Input
                  id="document"
                  value={formData.document}
                  onChange={(e) => setFormData({...formData, document: e.target.value})}
                  placeholder="000.000.000-00 ou 00.000.000/0000-00"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  placeholder="fornecedor@email.com"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="phone">Telefone</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  placeholder="(11) 99999-9999"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="address">Endereço</Label>
                <Input
                  id="address"
                  value={formData.address}
                  onChange={(e) => setFormData({...formData, address: e.target.value})}
                  placeholder="Endereço completo"
                />
              </div>
              
              <div className="flex justify-end space-x-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsDialogOpen(false)}
                >
                  Cancelar
                </Button>
                <Button type="submit" disabled={formLoading}>
                  {formLoading ? 'Salvando...' : 'Salvar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Lista de Fornecedores</CardTitle>
          <CardDescription>
            Gerencie os fornecedores da sua empresa
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2 mb-4">
            <Search className="h-4 w-4 text-gray-400" />
            <Input
              placeholder="Buscar por nome, documento ou email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-sm"
            />
          </div>

          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Fornecedor</TableHead>
                  <TableHead>Documento</TableHead>
                  <TableHead>Contato</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredSuppliers.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-8 text-gray-500">
                      {searchTerm ? 'Nenhum fornecedor encontrado' : 'Nenhum fornecedor cadastrado'}
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredSuppliers.map((supplier) => (
                    <TableRow key={supplier.id}>
                      <TableCell>
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                            {getDocumentType(supplier.document) === 'CPF' ? (
                              <User className="h-4 w-4 text-green-600" />
                            ) : (
                              <Building className="h-4 w-4 text-green-600" />
                            )}
                          </div>
                          <div>
                            <div className="font-medium">{supplier.name}</div>
                            {supplier.address && (
                              <div className="text-sm text-gray-500 flex items-center">
                                <MapPin className="h-3 w-3 mr-1" />
                                {supplier.address.substring(0, 50)}...
                              </div>
                            )}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div>
                          <Badge variant="outline">
                            {getDocumentType(supplier.document)}
                          </Badge>
                          <div className="text-sm font-mono mt-1">
                            {formatDocument(supplier.document)}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          {supplier.email && (
                            <div className="text-sm flex items-center">
                              <Mail className="h-3 w-3 mr-1 text-gray-400" />
                              {supplier.email}
                            </div>
                          )}
                          {supplier.phone && (
                            <div className="text-sm flex items-center">
                              <Phone className="h-3 w-3 mr-1 text-gray-400" />
                              {supplier.phone}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEdit(supplier)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(supplier)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Suppliers;

