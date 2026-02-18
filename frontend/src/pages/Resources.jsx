import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getResources, deleteResource } from '../services/api';
import Navbar from '../components/Navbar';
import '../App.css';

const Resources = () => {
    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const isAdmin = localStorage.getItem('user_role') === 'ADMIN';

    useEffect(() => {
        fetchResources();
    }, []);

    const fetchResources = async () => {
        try {
            const response = await getResources();
            setResources(response.data);
        } catch (err) {
            setError('Failed to load resources. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this resource?')) return;
        try {
            await deleteResource(id);
            setResources(prev => prev.filter(r => r.id !== id));
        } catch (err) {
            console.error(err);
            alert('Failed to delete resource');
        }
    };

    return (
        <div className="page-container">
            <Navbar />
            <div className="content-wrap">
                <div className="resource-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <h1>Campus Resources</h1>
                    {isAdmin && (
                        <Link to="/create-resource" className="login-btn" style={{ padding: '10px 20px', textDecoration: 'none', width: 'auto' }}>
                            + Add Resource
                        </Link>
                    )}
                </div>

                {loading && <p>Loading resources...</p>}
                {error && (
                    <div className="status unavailable" style={{ display: 'block', textAlign: 'center', margin: '2rem 0', padding: '1rem' }}>
                        {error}
                    </div>
                )}

                <div className="resource-grid">
                    {resources.map(resource => (
                        <div key={resource.id} className="resource-card" style={{ position: 'relative' }}>
                            <h3>{resource.name}</h3>
                            <p className="resource-type">{resource.type}</p>
                            <p>Capacity: {resource.capacity}</p>
                            <p className={`status ${resource.status.toLowerCase()}`}>
                                {resource.status}
                            </p>
                            <Link to={`/book/${resource.id}`} className="book-btn">Book Now</Link>

                            {isAdmin && (
                                <button
                                    onClick={() => handleDelete(resource.id)}
                                    style={{
                                        position: 'absolute',
                                        top: '10px',
                                        right: '10px',
                                        background: '#ff4757',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '50%',
                                        width: '24px',
                                        height: '24px',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        fontSize: '12px'
                                    }}
                                    title="Delete Resource"
                                >
                                    ✕
                                </button>
                            )}
                        </div>
                    ))}
                    {!loading && resources.length === 0 && !error && (
                        <div style={{ textAlign: 'center', gridColumn: '1 / -1', padding: '3rem', color: 'rgba(255,255,255,0.6)' }}>
                            <h3 style={{ marginBottom: '1rem' }}>No Resources Available</h3>
                            <p>Check back later for new campus facilities.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Resources;
