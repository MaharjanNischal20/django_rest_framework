import React, { useEffect, useState } from 'react';
import { fetchEvents } from '../api';
import EventItem from './EventItem';
import styles from './EventList.module.css'; // Import CSS Module

const EventList = ({ setEvent }) => {
  const [events, setEvents] = useState([]);
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [filters, setFilters] = useState({ title: '', startDate: '', endDate: '' });

  const fetchAllEvents = async () => {
    try {
      const response = await fetchEvents();
      setEvents(response.data.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchAllEvents();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [events, filters]);

  const applyFilters = () => {
    const filtered = events.filter(event =>
      event.title.toLowerCase().includes(filters.title.toLowerCase()) &&
      event.start_date.includes(filters.startDate) &&
      event.end_date.includes(filters.endDate)
    );
    setFilteredEvents(filtered);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  return (
    <div>
      <div>
        <h3>Filter Events</h3>
        <input
          type="text"
          name="title"
          value={filters.title}
          onChange={handleChange}
          placeholder="Filter by Title"
        />
        <input
          type="date"
          name="startDate"
          value={filters.startDate}
          onChange={handleChange}
          placeholder="Start Date"
        />
        <input
          type="date"
          name="endDate"
          value={filters.endDate}
          onChange={handleChange}
          placeholder="End Date"
        />
      </div>
      <div>
        <h2>Events</h2>
        {filteredEvents.map((event) => (
          <EventItem key={event.id} event={event} setEvent={setEvent} fetchEvents={fetchAllEvents} />
        ))}
      </div>
    </div>
  );
};

export default EventList;
