import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    pendingTasks: 0,
    upcomingEvents: 0,
    todayWorkouts: 0,
    todayMeals: 0
  });
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [pendingTasks, setPendingTasks] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch tasks
      const tasksRes = await axios.get('/api/tasks?status=pending');
      setPendingTasks(tasksRes.data.slice(0, 5));
      setStats(prev => ({ ...prev, pendingTasks: tasksRes.data.length }));

      // Fetch upcoming events
      const eventsRes = await axios.get('/api/events/upcoming/next?limit=5');
      setUpcomingEvents(eventsRes.data);
      setStats(prev => ({ ...prev, upcomingEvents: eventsRes.data.length }));
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Pending Tasks</h3>
          <div className="stat-number">{stats.pendingTasks}</div>
        </div>
        <div className="stat-card">
          <h3>Upcoming Events</h3>
          <div className="stat-number">{stats.upcomingEvents}</div>
        </div>
        <div className="stat-card">
          <h3>Today's Workouts</h3>
          <div className="stat-number">{stats.todayWorkouts}</div>
        </div>
        <div className="stat-card">
          <h3>Today's Meals</h3>
          <div className="stat-number">{stats.todayMeals}</div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="card">
          <h2>Pending Tasks</h2>
          {pendingTasks.length === 0 ? (
            <p>No pending tasks</p>
          ) : (
            <ul className="task-list">
              {pendingTasks.map(task => (
                <li key={task.id} className={`priority-${task.priority}`}>
                  <strong>{task.title}</strong>
                  <span className="task-priority">{task.priority}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card">
          <h2>Upcoming Events</h2>
          {upcomingEvents.length === 0 ? (
            <p>No upcoming events</p>
          ) : (
            <ul className="event-list">
              {upcomingEvents.map(event => (
                <li key={event.id}>
                  <strong>{event.title}</strong>
                  <span className="event-time">
                    {new Date(event.start_time).toLocaleString()}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button className="btn btn-primary" onClick={() => window.location.href = '/tasks'}>
            Add Task
          </button>
          <button className="btn btn-primary" onClick={() => window.location.href = '/calendar'}>
            Add Event
          </button>
          <button className="btn btn-primary" onClick={() => window.location.href = '/meals'}>
            Log Meal
          </button>
          <button className="btn btn-primary" onClick={() => window.location.href = '/workouts'}>
            Log Workout
          </button>
          <button className="btn btn-success" onClick={() => window.location.href = '/chat'}>
            Chat with AI
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
