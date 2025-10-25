import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      const response = await axios.get('/api/workouts');
      setWorkouts(response.data);
    } catch (error) {
      console.error('Error fetching workouts:', error);
    }
  };

  const generateWorkoutPlan = async () => {
    try {
      await axios.post('/api/workouts/plans', {
        name: 'Fitness Plan',
        start_date: new Date().toISOString(),
        fitness_level: 'intermediate',
        goals: ['strength', 'endurance']
      });
      alert('Workout plan generated successfully!');
    } catch (error) {
      console.error('Error generating workout plan:', error);
    }
  };

  return (
    <div>
      <h1>Workouts & Exercise</h1>
      <div className="card">
        <h2>AI Workout Planning</h2>
        <p>Get personalized workout plans based on your fitness level and goals.</p>
        <button className="btn btn-success" onClick={generateWorkoutPlan}>
          Generate Workout Plan
        </button>
      </div>
      <div className="card">
        <h2>Recent Workouts</h2>
        {workouts.length === 0 ? (
          <p>No workouts logged yet.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {workouts.map(workout => (
              <li key={workout.id} style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>
                <strong>{workout.name}</strong> - {workout.workout_type}
                {workout.duration && <span style={{ marginLeft: '1rem', color: '#666' }}>
                  {workout.duration} min
                </span>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Workouts;
