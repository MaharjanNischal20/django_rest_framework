import React from 'react';
import { deleteEvent } from '../api';
import styles from './EventItem.module.css'; // Import CSS Module

const EventItem = ({ event, setEvent, fetchEvents }) => {
  const handleDelete = async () => {
    try {
      await deleteEvent(event.id);
      fetchEvents();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className={styles.eventItem}>
      <h3>{event.title}</h3>
      <p>{event.description}</p>
      <p>Participants: {event.participants}</p>
      <p>Start Date: {event.start_date}</p>
      <p>End Date: {event.end_date}</p>
      <button onClick={() => setEvent(event)} className={styles.editButton}>Edit</button>
      <button onClick={handleDelete} className={styles.deleteButton}>Delete</button>
    </div>
  );
};

export default EventItem;
