import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Resources from './pages/Resources';
import Bookings from './pages/Bookings';
import CreateBooking from './pages/CreateBooking';
import CreateResource from './pages/CreateResource';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/create-resource" element={<CreateResource />} />
        <Route path="/book/:resourceId" element={<CreateBooking />} />
        <Route path="/bookings" element={<Bookings />} />
      </Routes>
    </Router>
  )
}

export default App
