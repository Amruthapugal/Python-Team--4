import React, { useEffect, useState } from 'react';
import { getBookings, approveBooking, rejectBooking } from '../services/api';
import Navbar from '../components/Navbar';
import '../App.css';

const Bookings = () => {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        const role = localStorage.getItem('user_role');
        setIsAdmin(role === 'STAFF' || role === 'ADMIN');

        const fetchBookings = async () => {
            try {
                const response = await getBookings();
                setBookings(response.data);
            } catch (err) {
                setError('Failed to load bookings.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchBookings();
    }, []);

    const handleAction = async (id, action) => {
        if (!window.confirm(`Are you sure you want to ${action} this booking?`)) return;

        try {
            if (action === 'approve') await approveBooking(id);
            if (action === 'reject') await rejectBooking(id);

            // Refresh list or optimistic update
            setBookings(prev => prev.map(b =>
                b.id === id ? { ...b, status: action === 'approve' ? 'APPROVED' : 'REJECTED' } : b
            ));
        } catch (err) {
            console.error(err);
            alert(`Failed to ${action} booking.`);
        }
    };

    return (
        <div className="page-container">
            <Navbar />
            <div className="content-wrap">
                <h1>{isAdmin ? 'Booking Management' : 'My Bookings'}</h1>
                {loading && <p>Loading bookings...</p>}
                {error && (
                    <div className="status unavailable" style={{ display: 'block', textAlign: 'center', margin: '2rem 0', padding: '1rem' }}>
                        {error} <br /> <small>Please log in again if this persists.</small>
                    </div>
                )}

                <div className="booking-list">
                    {bookings.map(booking => (
                        <div key={booking.id} className="booking-item" style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                            <div className="booking-header" style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center', marginBottom: '10px' }}>
                                <div className="booking-info">
                                    <h3>{booking.resource_name || `Resource #${booking.resource}`}</h3>
                                    {isAdmin && booking.user_email && (
                                        <p style={{ color: '#aaa', fontSize: '0.9rem' }}>User: {booking.user_name} ({booking.user_email})</p>
                                    )}
                                    <p>Date: {booking.booking_date}</p>
                                    <p>Time: {booking.time_slot}</p>
                                </div>
                                <div className={`booking-status ${booking.status.toLowerCase()}`}>
                                    {booking.status}
                                </div>
                            </div>

                            {isAdmin && booking.status === 'PENDING' && (
                                <div className="booking-actions" style={{ display: 'flex', gap: '10px', width: '100%', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '10px' }}>
                                    <button
                                        onClick={() => handleAction(booking.id, 'approve')}
                                        style={{ background: '#4CAF50', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', flex: 1 }}
                                    >
                                        Approve
                                    </button>
                                    <button
                                        onClick={() => handleAction(booking.id, 'reject')}
                                        style={{ background: '#f44336', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', flex: 1 }}
                                    >
                                        Reject
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                    {!loading && bookings.length === 0 && !error && (
                        <div style={{ textAlign: 'center', padding: '3rem', color: 'rgba(255,255,255,0.6)' }}>
                            <h3 style={{ marginBottom: '1rem' }}>No Bookings Yet</h3>
                            <p>You haven't made any bookings. Visit the <Link to="/resources" style={{ color: '#fff' }}>Resources</Link> page to verify.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Bookings;
