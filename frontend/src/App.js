import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Import pages
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Calendar from './pages/Calendar';
import Email from './pages/Email';
import Meals from './pages/Meals';
import Workouts from './pages/Workouts';
import Chat from './pages/Chat';
import Schedule from './pages/Schedule';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="navbar-brand">
            <h2>AI Personal Assistant</h2>
          </div>
          <ul className="navbar-menu">
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/tasks">Tasks</Link></li>
            <li><Link to="/calendar">Calendar</Link></li>
            <li><Link to="/email">Email</Link></li>
            <li><Link to="/meals">Meals</Link></li>
            <li><Link to="/workouts">Workouts</Link></li>
            <li><Link to="/schedule">Schedule</Link></li>
            <li><Link to="/chat">Chat</Link></li>
          </ul>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/email" element={<Email />} />
            <Route path="/meals" element={<Meals />} />
            <Route path="/workouts" element={<Workouts />} />
            <Route path="/schedule" element={<Schedule />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
