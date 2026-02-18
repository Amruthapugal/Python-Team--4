import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createBooking, getResources } from '../services/api';
import Navbar from '../components/Navbar';
import '../App.css';

const CreateBooking = () => {
    const { resourceId } = useParams();
    const navigate = useNavigate();
    const [resourceName, setResourceName] = useState('');
    const [bookingDate, setBookingDate] = useState('');
    const [timeSlot, setTimeSlot] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Fetch resource details to show name
        const fetchResource = async () => {
            try {
                const response = await getResources();
                const resource = response.data.find(r => r.id === parseInt(resourceId));
                if (resource) {
                    setResourceName(resource.name);
                } else {
                    setError('Resource not found.');
                }
            } catch (err) {
                console.error('Failed to fetch resource details', err);
            }
        };
        fetchResource();
    }, [resourceId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await createBooking({
                resource: resourceId,
                booking_date: bookingDate,
                time_slot: timeSlot
            });
            alert('Booking created successfully!'); // Simple notification
            navigate('/bookings');
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data) {
                // Try to formulate a better error message from DRF response
                const msg = JSON.stringify(err.response.data);
                setError(`Booking failed: ${msg}`);
            } else {
                setError('Failed to create booking. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <Navbar />
            <div className="content-wrap auth-container"> {/* Reusing auth-container for form style */}
                <h1>Book {resourceName}</h1>
                <form onSubmit={handleSubmit} className="auth-form"> {/* Reusing auth-form style */}
                    {error && <p className="error-msg">{error}</p>}

                    <div className="form-group">
                        <label>Date:</label>
                        <input
                            type="date"
                            value={bookingDate}
                            onChange={(e) => setBookingDate(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Time Slot:</label>
                        <input
                            type="text"
                            placeholder="e.g. 10:00-11:00"
                            value={timeSlot}
                            onChange={(e) => setTimeSlot(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" className="auth-btn" disabled={loading}>
                        {loading ? 'Booking...' : 'Confirm Booking'}
                    </button>
                    <button type="button" className="nav-btn cancel-btn" onClick={() => navigate('/resources')}>Cancel</button>
                </form>
            </div>
        </div>
    );
};

export default CreateBooking;
