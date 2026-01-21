'use client';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import Link from 'next/link';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await login(username, password);
    if (!res.success) {
      setError(res.error);
    }
  };

  return (
    <div className="login-container" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', padding: '20px'}}>
      <div className="card" style={{background: 'rgba(30, 30, 30, 0.95)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', maxWidth: '400px', width: '100%'}}>
        <div className="card-header" style={{background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)', color: '#fff', textAlign: 'center', padding: '30px 20px', fontSize: '24px'}}>Welcome Back</div>
        <div className="card-body" style={{padding: '40px 30px'}}>
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group" style={{marginBottom: '24px'}}>
              <label htmlFor="username" style={{display: 'block', marginBottom: '8px', color: '#b0b0b0'}}>Username</label>
              <input
                type="text"
                className="form-control"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={{background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', color: '#fff'}}
              />
            </div>
            <div className="form-group" style={{marginBottom: '24px'}}>
              <label htmlFor="password" style={{display: 'block', marginBottom: '8px', color: '#b0b0b0'}}>Password</label>
              <input
                type="password"
                className="form-control"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', color: '#fff'}}
              />
            </div>
            <button type="submit" className="btn btn-primary btn-block" style={{background: 'linear-gradient(135deg, #4a9eff 0%, #357abd 100%)', border: 'none', padding: '14px', fontSize: '16px'}}>Sign In</button>
            <div className="register-link" style={{textAlign: 'center', marginTop: '20px', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.1)'}}>
              <span style={{color: '#888'}}>Don't have an account?</span>
              <Link href="/register" style={{color: '#4a9eff', marginLeft: '8px'}}>Create one</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
