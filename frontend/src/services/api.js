import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to attach the token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle 401 errors (Token expired/invalid)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Token is invalid or expired
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            // Redirect to login if not already there
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export const login = (email, password) => {
    return api.post('/token/', { email, password });
};

export const registerUser = (userData) => {
    return api.post('/users/', userData);
};

export const getResources = () => {
    return api.get('/resources/');
};

export const createResource = (resourceData) => {
    return api.post('/resources/', resourceData);
};

export const getBookings = () => {
    return api.get('/bookings/');
};

export const createBooking = (bookingData) => {
    return api.post('/bookings/', bookingData);
};

export const approveBooking = (id) => {
    return api.post(`/bookings/${id}/approve/`);
};

export const rejectBooking = (id) => {
    return api.post(`/bookings/${id}/reject/`);
};

export const deleteResource = (id) => {
    return api.delete(`/resources/${id}/`);
};

export default api;
