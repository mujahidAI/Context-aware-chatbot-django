'use client';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import Link from 'next/link';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState('');
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== passwordConfirm) {
      setError("Passwords don't match");
      return;
    }
    const res = await register(username, email, password);
    if (!res.success) {
        if (typeof res.error === 'object') {
            setError(JSON.stringify(res.error));
        } else {
            setError(res.error);
        }
    }
  };

  return (
    <div className="register-container" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', padding: '20px'}}>
      <div className="card" style={{background: 'rgba(30, 30, 30, 0.95)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', maxWidth: '420px', width: '100%'}}>
        <div className="card-header" style={{background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)', color: '#fff', textAlign: 'center', padding: '30px 20px', fontSize: '24px'}}>Create Account</div>
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
              <label htmlFor="email" style={{display: 'block', marginBottom: '8px', color: '#b0b0b0'}}>Email Address</label>
              <input
                type="email"
                className="form-control"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
            <div className="form-group" style={{marginBottom: '24px'}}>
              <label htmlFor="passwordConfirm" style={{display: 'block', marginBottom: '8px', color: '#b0b0b0'}}>Confirm Password</label>
              <input
                type="password"
                className="form-control"
                id="passwordConfirm"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
                style={{background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', color: '#fff'}}
              />
            </div>
            <button type="submit" className="btn btn-primary btn-block" style={{background: 'linear-gradient(135deg, #4a9eff 0%, #357abd 100%)', border: 'none', padding: '14px', fontSize: '16px'}}>Create Account</button>
            <div className="login-link" style={{textAlign: 'center', marginTop: '20px', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.1)'}}>
              <span style={{color: '#888'}}>Already have an account?</span>
              <Link href="/login" style={{color: '#4a9eff', marginLeft: '8px'}}>Sign in</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
