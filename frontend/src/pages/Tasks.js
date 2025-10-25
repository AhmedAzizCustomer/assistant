import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium',
    category: '',
    due_date: ''
  });

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get('/api/tasks');
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const createTask = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/tasks', newTask);
      setNewTask({ title: '', description: '', priority: 'medium', category: '', due_date: '' });
      setShowForm(false);
      fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      await axios.put(`/api/tasks/${taskId}`, { status: newStatus });
      fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const deleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await axios.delete(`/api/tasks/${taskId}`);
        fetchTasks();
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <h1>Tasks</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add Task'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Create New Task</h2>
          <form onSubmit={createTask}>
            <input
              type="text"
              placeholder="Task title"
              value={newTask.title}
              onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
              required
            />
            <textarea
              placeholder="Description"
              value={newTask.description}
              onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
              rows="3"
            />
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
            >
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
              <option value="urgent">Urgent</option>
            </select>
            <input
              type="text"
              placeholder="Category (e.g., work, personal)"
              value={newTask.category}
              onChange={(e) => setNewTask({ ...newTask, category: e.target.value })}
            />
            <input
              type="datetime-local"
              value={newTask.due_date}
              onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
            />
            <button type="submit" className="btn btn-success">Create Task</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>All Tasks</h2>
        {tasks.length === 0 ? (
          <p>No tasks yet. Create your first task!</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Title</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Priority</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Status</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Due Date</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(task => (
                <tr key={task.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '0.75rem' }}>
                    <strong>{task.title}</strong>
                    {task.description && <div style={{ fontSize: '0.85rem', color: '#666' }}>{task.description}</div>}
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <span className={`task-priority priority-${task.priority}`}>{task.priority}</span>
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <select
                      value={task.status}
                      onChange={(e) => updateTaskStatus(task.id, e.target.value)}
                      style={{ padding: '0.25rem' }}
                    >
                      <option value="pending">Pending</option>
                      <option value="in_progress">In Progress</option>
                      <option value="completed">Completed</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date'}
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <button
                      className="btn btn-danger"
                      onClick={() => deleteTask(task.id)}
                      style={{ padding: '0.25rem 0.75rem', fontSize: '0.85rem' }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Tasks;
