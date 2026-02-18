import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import "../App.css"; // Reusing existing styles

const Navbar = () => {
    const location = useLocation();
    const isHomePage = location.pathname === '/';

    const scrollToSection = (sectionId) => {
        if (!isHomePage) {
            // If not on home page, just navigate to home (scrolling would need more complex handling or context)
            // For now, let's keep it simple: The links Features/About/Contact only work on Home.
            window.location.href = `/#${sectionId}`;
        } else {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    };

    return (
        <nav className="navbar">
            <Link to="/" className="logo">
                <span className="logo-icon">M</span> CampusSys
                {localStorage.getItem('user_role') === 'ADMIN' && <span style={{ fontSize: '0.8rem', background: '#ff4757', padding: '2px 8px', borderRadius: '4px', marginLeft: '8px', verticalAlign: 'middle' }}>ADMIN</span>}
            </Link>
            <div className="nav-links">
                {/* Using anchor tags for sections on the same page */}
                <a href="#productivity" onClick={(e) => { e.preventDefault(); scrollToSection('features'); }}>Features</a>
                <a href="#workplace" onClick={(e) => { e.preventDefault(); scrollToSection('about'); }}>About</a>
                <a href="#security" onClick={(e) => { e.preventDefault(); scrollToSection('contact'); }}>Contact</a>

                <Link to="/resources" className="nav-link">Resources</Link>
                <Link to="/bookings" className="nav-link">My Bookings</Link>
                {localStorage.getItem('access_token') ? (
                    <button onClick={() => {
                        localStorage.removeItem('access_token');
                        localStorage.removeItem('refresh_token');
                        window.location.href = '/login';
                    }} className="nav-btn" style={{ cursor: 'pointer' }}>Logout</button>
                ) : (
                    <Link to="/login" className="nav-btn">Login</Link>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
