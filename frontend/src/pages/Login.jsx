import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';
import '../App.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await api.post('/token/', {
                email: username.trim(),
                password: password.trim()
            });

            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('user_role', response.data.role);
            localStorage.setItem('user_name', response.data.name);
            localStorage.setItem('user_email', response.data.email);

            // Redirect to dashboard or home
            navigate('/');
            alert('Login Successful!');
        } catch (err) {
            console.error('Login failed', err);
            setError('Invalid credentials. Please try again.');
        }
    };

    return (
        <div className="app-container">
            <Navbar />

            <div className="login-container">
                <div className="login-card">
                    <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Welcome Back 👋</h2>
                    <p className="login-subtitle">Login to continue</p>

                    {error && <div style={{ color: 'red', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}

                    <form onSubmit={handleSubmit} className="login-form">
                        <div className="form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Enter your email"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter your password"
                                required
                            />
                        </div>

                        <div className="form-actions">
                            <a href="#" className="forgot-password">Forgot Password?</a>
                        </div>

                        <button type="submit" className="login-btn">Sign In</button>

                        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                            <p>Don't have an account? <Link to="/register" style={{ color: '#fff' }}>Sign Up</Link></p>
                        </div>
                    </form>
                </div>

                {/* Visual decoration */}
                <div className="glow-effect" style={{
                    top: '50%',
                    left: '50%',
                    width: '300px',
                    height: '300px',
                    transform: 'translate(-50%, -50%)',
                    zIndex: -1
                }}></div>
            </div>
        </div>
    );
};

export default Login;
