import React, { useState } from 'react';
import axios from 'axios';

function Schedule() {
  const [optimizedSchedule, setOptimizedSchedule] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const optimizeSchedule = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post('/api/schedule/optimize', {
        start_date: new Date().toISOString(),
        end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        work_hours_start: '09:00',
        work_hours_end: '17:00',
        include_tasks: true,
        include_workouts: true,
        include_meals: true
      });
      setOptimizedSchedule(response.data);
    } catch (error) {
      console.error('Error optimizing schedule:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1>Schedule Planning</h1>
      <div className="card">
        <h2>AI Schedule Optimization</h2>
        <p>Let AI optimize your schedule for maximum productivity and work-life balance.</p>
        <button
          className="btn btn-success"
          onClick={optimizeSchedule}
          disabled={isLoading}
        >
          {isLoading ? 'Optimizing...' : 'Optimize My Schedule'}
        </button>
      </div>

      {optimizedSchedule && (
        <div className="card">
          <h2>Optimized Schedule</h2>
          <pre style={{ background: '#f5f5f5', padding: '1rem', borderRadius: '4px', overflow: 'auto' }}>
            {JSON.stringify(optimizedSchedule, null, 2)}
          </pre>
        </div>
      )}

      <div className="card">
        <h2>Features</h2>
        <ul>
          <li>Intelligent task scheduling based on priority and deadlines</li>
          <li>Automatic meeting conflict detection</li>
          <li>Work-life balance optimization</li>
          <li>Energy level-based task placement</li>
          <li>Meal and workout time integration</li>
        </ul>
      </div>
    </div>
  );
}

export default Schedule;
