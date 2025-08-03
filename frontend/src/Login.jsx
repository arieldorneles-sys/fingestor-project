import React, { useState } from 'react';

export default function Login() {
  const [email] = useState('admin@empresaexemplo.com.br');
  const [password] = useState('admin123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    setLoading(true);
    setError(null);

    try {
      // Aqui você pode chamar sua API para autenticar, ex:
      // const response = await api.login({ email, password });
      // Se usar fetch:
      /*
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) throw new Error('Erro ao autenticar');
      */

      // Simulando login bem-sucedido:
      await new Promise((r) => setTimeout(r, 1000));

      alert('Login realizado com sucesso!');
      // Redirecionar para dashboard, ex:
      // window.location.href = '/dashboard';
    } catch (err) {
      setError('Falha no login. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>FinGestor</h1>
      <p><b>Sistema ERP Financeiro</b></p>

      <div style={styles.box}>
        <label>
          E-mail:
          <input type="email" value={email} readOnly style={styles.input} />
        </label>
        <label>
          Senha:
          <input type="password" value={password} readOnly style={styles.input} />
        </label>

        <button onClick={handleLogin} disabled={loading} style={styles.button}>
          {loading ? 'Entrando...' : 'Entrar no Sistema'}
        </button>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <p style={styles.info}>
          Os dados já estão preenchidos para demonstração.<br/>
          Certifique-se que o backend está rodando na porta 8000.
        </p>
      </div>

      <footer style={styles.footer}>
        © 2025 FinGestor - Sistema ERP Financeiro
      </footer>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 400,
    margin: 'auto',
    padding: 20,
    fontFamily: 'Arial, sans-serif',
    textAlign: 'center',
  },
  box: {
    border: '1px solid #ccc',
    borderRadius: 8,
    padding: 20,
    marginTop: 20,
  },
  input: {
    display: 'block',
    width: '100%',
    padding: 8,
    marginTop: 4,
    marginBottom: 12,
    fontSize: 16,
  },
  button: {
    width: '100%',
    padding: 10,
    fontSize: 16,
    cursor: 'pointer',
    backgroundColor: '#536879',
    color: '#fff',
    border: 'none',
    borderRadius: 5,
  },
  info: {
    marginTop: 12,
    fontSize: 14,
    color: '#666',
  },
  footer: {
    marginTop: 40,
    fontSize: 12,
    color: '#999',
  },
};
