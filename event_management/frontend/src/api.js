import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const getAuthHeaders = () => ({
  headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
});

export const fetchEvents = () => axios.get(`${API_URL}/events/`, getAuthHeaders());
export const createEvent = (event) => axios.post(`${API_URL}/events/`, event, getAuthHeaders());
export const updateEvent = (id, event) => axios.put(`${API_URL}/events/${id}/`, event, getAuthHeaders());
export const deleteEvent = (id) => axios.delete(`${API_URL}/events/${id}/`, getAuthHeaders());
