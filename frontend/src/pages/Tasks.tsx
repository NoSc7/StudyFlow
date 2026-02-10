import { useState } from 'react';

interface Task {
  id: number;
  title: string;
  course: string;
  completed: boolean;
}

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, title: 'Lire le chapitre 3', course: 'Mathématiques', completed: false },
    { id: 2, title: 'Faire les exercices', course: 'Français', completed: true },
    { id: 3, title: 'Réviser vocabulaire', course: 'Anglais', completed: false },
  ]);

  const toggleTask = (id: number) => {
    setTasks(tasks.map((task) => (task.id === id ? { ...task, completed: !task.completed } : task)));
  };

  return (
    <div className="page-tasks">
      <h2>Mes tâches</h2>
      <p>Suis et valide tes tâches d'étude.</p>
      <div className="tasks-list">
        {tasks.map((task) => (
          <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleTask(task.id)}
            />
            <div className="task-info">
              <h3>{task.title}</h3>
              <p>{task.course}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}