import React, { useState } from 'react';
import axios from 'axios';
import styles from './LoginForm.module.css'; // Import CSS Module

const LoginForm = ({ setToken }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/token/', {
        username,
        password
      });
      setToken(response.data.access);
      localStorage.setItem('token', response.data.access);
    } catch (error) {
      console.error('Login failed', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.loginForm}>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className={styles.inputField}
        placeholder="Username"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className={styles.inputField}
        placeholder="Password"
        required
      />
      <button type="submit" className={styles.loginButton}>Login</button>
    </form>
  );
};

export default LoginForm;
