import React, { useState, useEffect } from 'react';
import { createEvent, updateEvent } from '../api';
import styles from './EventForm.module.css'; // Import CSS Module

const EventForm = ({ event, setEvent, fetchEvents }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    participants: 0,
    start_date: '',
    end_date: '',
  });

  useEffect(() => {
    if (event) {
      setFormData(event);
    }
  }, [event]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (event) {
        await updateEvent(event.id, formData);
        setEvent(null);
      } else {
        await createEvent(formData);
      }
      fetchEvents();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.eventForm}>
      <label htmlFor="title">Title</label>
      <input
        type="text"
        name="title"
        value={formData.title}
        onChange={handleChange}
        required
        className={styles.inputField}
      />
      <label htmlFor="description">Description</label>
      <textarea
        name="description"
        value={formData.description}
        onChange={handleChange}
        required
        className={styles.textareaField}
      ></textarea>
      <label htmlFor="participants">Participants</label>
      <input
        type="number"
        name="participants"
        value={formData.participants}
        onChange={handleChange}
        required
        className={styles.inputField}
      />
      <label htmlFor="start_date">Start Date</label>
      <input
        type="date"
        name="start_date"
        value={formData.start_date}
        onChange={handleChange}
        required
        className={styles.inputField}
      />
      <label htmlFor="end_date">End Date</label>
      <input
        type="date"
        name="end_date"
        value={formData.end_date}
        onChange={handleChange}
        required
        className={styles.inputField}
      />
      <button type="submit" className={styles.submitButton}>
        {event ? 'Update' : 'Create'} Event
      </button>
    </form>
  );
};

export default EventForm;
