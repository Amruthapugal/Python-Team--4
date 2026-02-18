import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { createResource } from '../services/api';
import '../App.css';

const CreateResource = () => {
    const [name, setName] = useState('');
    const [type, setType] = useState('CLASSROOM');
    const [capacity, setCapacity] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Check if user is admin, else redirect
    const isAdmin = localStorage.getItem('user_role') === 'ADMIN';
    if (!isAdmin) {
        // Simple client-side check. Backend also protects the endpoint.
        return (
            <div className="page-container">
                <Navbar />
                <div className="content-wrap">
                    <h1>Access Denied</h1>
                    <p>Only administrators can create resources.</p>
                </div>
            </div>
        );
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await createResource({
                name,
                type,
                capacity: parseInt(capacity),
                status: 'AVAILABLE'
            });
            alert('Resource created successfully!');
            navigate('/resources');
        } catch (err) {
            console.error(err);
            setError('Failed to create resource. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <Navbar />
            <div className="content-wrap">
                <h1>Add New Resource</h1>

                {error && <div className="error-message" style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

                <form onSubmit={handleSubmit} className="booking-form" style={{ maxWidth: '500px', margin: '0 auto' }}>
                    <div className="form-group">
                        <label>Resource Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="e.g., Computer Lab 101"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Type</label>
                        <select value={type} onChange={(e) => setType(e.target.value)}>
                            <option value="CLASSROOM">Classroom</option>
                            <option value="LAB">Lab</option>
                            <option value="EVENT_HALL">Event Hall</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Capacity</label>
                        <input
                            type="number"
                            value={capacity}
                            onChange={(e) => setCapacity(e.target.value)}
                            placeholder="e.g., 30"
                            min="1"
                            required
                        />
                    </div>

                    <button type="submit" className="login-btn" disabled={loading}>
                        {loading ? 'Creating...' : 'Create Resource'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default CreateResource;
