import React from 'react';
import Navbar from '../components/Navbar';
import '../App.css';

const Home = () => {
    return (
        <div className="app-container">
            <Navbar />

            <main className="hero-section">
                <div className="hero-content">
                    <h1>
                        Manage your <br />
                        <span className="gradient-text">Campus Life</span> <br />
                        effortlessly.
                    </h1>
                    <p className="hero-subtitle">
                        A comprehensive system for students and faculty to manage resources,
                        bookings, and schedules with ease.
                    </p>

                    <div className="hero-cta">
                        <button className="play-btn">
                            <div className="play-icon">▶</div>
                        </button>
                        <span>Watch Demo</span>
                    </div>
                </div>

                <div className="hero-visuals">
                    <div className="floating-card card-1">
                        <div className="card-content">
                            <h3>Student Portal</h3>
                            <div className="progress-bar"><div className="fill" style={{ width: '75%' }}></div></div>
                        </div>
                    </div>
                    <div className="floating-card card-2">
                        <div className="card-icon">📅</div>
                        <h3>Schedule</h3>
                    </div>
                    <div className="floating-card card-3">
                        <div className="card-icon">📚</div>
                        <h3>Resources</h3>
                    </div>
                    <div className="glow-effect"></div>
                </div>
            </main>

            {/* Placeholder Sections for Scrolling */}
            <section id="features" style={{ padding: '4rem 0', minHeight: '50vh' }}>
                <h2 className="section-title">Features</h2>
                <div className="grid-container">
                    <div className="feature-card">Real-time Booking</div>
                    <div className="feature-card">Resource Tracking</div>
                    <div className="feature-card">Event Management</div>
                </div>
            </section>

            <section id="about" style={{ padding: '4rem 0', minHeight: '50vh' }}>
                <h2 className="section-title">About Us</h2>
                <p style={{ color: 'rgba(255,255,255,0.7)', maxWidth: '600px' }}>
                    CampusSys is dedicated to streamlining interaction between students, faculty, and campus resources through modern technology.
                </p>
            </section>

            <section id="contact" style={{ padding: '4rem 0', minHeight: '50vh', marginBottom: '4rem' }}>
                <h2 className="section-title">Contact</h2>
                <p style={{ color: 'rgba(255,255,255,0.7)' }}>support@campussys.com</p>
            </section>
        </div>
    );
};

export default Home;
