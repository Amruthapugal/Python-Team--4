import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { registerUser } from '../services/api';
import '../App.css';

const Register = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [role, setRole] = useState('STUDENT'); // Default role
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError("Passwords don't match!");
            return;
        }

        setLoading(true);

        try {
            await registerUser({
                username: email, // Using email as username
                email,
                name,
                password,
                role
            });

            alert('Registration Successful! Please login.');
            navigate('/login');
        } catch (err) {
            console.error('Registration failed', err);
            if (err.response && err.response.data) {
                // Formatting error message
                const msg = Object.entries(err.response.data)
                    .map(([key, value]) => `${key}: ${value}`)
                    .join(', ');
                setError(msg);
            } else {
                setError('Registration failed. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <Navbar />

            <div className="login-container">
                <div className="login-card">
                    <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Create Account 🚀</h2>
                    <p className="login-subtitle">Sign up to get started</p>

                    {error && <div style={{ color: 'red', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}

                    <form onSubmit={handleSubmit} className="login-form">
                        <div className="form-group">
                            <label>Full Name</label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Enter your full name"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
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
                                placeholder="Create a password"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm your password"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Role</label>
                            <select value={role} onChange={(e) => setRole(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}>
                                <option value="STUDENT">Student</option>
                                <option value="STAFF">Staff</option>
                                <option value="ADMIN">Admin</option>
                            </select>
                        </div>

                        <button type="submit" className="login-btn" disabled={loading}>
                            {loading ? 'Creating Account...' : 'Sign Up'}
                        </button>

                        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                            <p>Already have an account? <Link to="/login" style={{ color: '#007bff' }}>Login here</Link></p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Register;
