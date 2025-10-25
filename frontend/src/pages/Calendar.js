import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Calendar() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get('/api/events');
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  return (
    <div>
      <h1>Calendar & Events</h1>
      <div className="card">
        <h2>Upcoming Events</h2>
        {events.length === 0 ? (
          <p>No events scheduled.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {events.map(event => (
              <li key={event.id} style={{ padding: '1rem', borderBottom: '1px solid #eee' }}>
                <strong>{event.title}</strong>
                <div style={{ color: '#666', fontSize: '0.9rem' }}>
                  {new Date(event.start_time).toLocaleString()}
                  {event.location && ` - ${event.location}`}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Calendar;
