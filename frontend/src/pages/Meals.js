import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Meals() {
  const [meals, setMeals] = useState([]);
  const [showPlanGenerator, setShowPlanGenerator] = useState(false);

  useEffect(() => {
    fetchMeals();
  }, []);

  const fetchMeals = async () => {
    try {
      const response = await axios.get('/api/meals');
      setMeals(response.data);
    } catch (error) {
      console.error('Error fetching meals:', error);
    }
  };

  const generateMealPlan = async () => {
    try {
      const response = await axios.post('/api/meals/plans', {
        name: 'Weekly Meal Plan',
        start_date: new Date().toISOString(),
        end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        daily_calorie_target: 2000
      });
      alert('Meal plan generated successfully!');
    } catch (error) {
      console.error('Error generating meal plan:', error);
    }
  };

  return (
    <div>
      <h1>Meals & Nutrition</h1>
      <div className="card">
        <h2>AI Meal Planning</h2>
        <p>Generate personalized meal plans based on your dietary preferences and goals.</p>
        <button className="btn btn-success" onClick={generateMealPlan}>
          Generate Weekly Meal Plan
        </button>
      </div>
      <div className="card">
        <h2>Recent Meals</h2>
        {meals.length === 0 ? (
          <p>No meals logged yet.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {meals.map(meal => (
              <li key={meal.id} style={{ padding: '0.75rem', borderBottom: '1px solid #eee' }}>
                <strong>{meal.name}</strong> - {meal.meal_type}
                {meal.calories && <span style={{ marginLeft: '1rem', color: '#666' }}>
                  {meal.calories} cal
                </span>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Meals;
