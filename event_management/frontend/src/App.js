import React, { useState } from 'react';
import EventForm from './components/EventForm';
import EventList from './components/EventList';
import LoginForm from './components/LoginForm';
import { fetchEvents } from './api';  // Import fetchEvents


const App = () => {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  if (!token) {
    return <LoginForm setToken={setToken} />;
  }

  return (
    <div>
      <h1>Event Management</h1>
      <button onClick={handleLogout}>Logout</button>
      <EventForm event={selectedEvent} setEvent={setSelectedEvent} fetchEvents={fetchEvents} />
      <EventList setEvent={setSelectedEvent} />
    </div>
  );
};

export default App;
