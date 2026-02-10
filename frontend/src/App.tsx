import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>StudyFlow</h1>
          <p>Your Personal Study Assistant</p>
        </header>
        
        <nav className="app-nav">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/courses">Courses</a></li>
            <li><a href="/tasks">Tasks</a></li>
            <li><a href="/profile">Profile</a></li>
          </ul>
        </nav>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomeContent />} />
            <Route path="/courses" element={<CoursesContent />} />
            <Route path="/tasks" element={<TasksContent />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>&copy; 2026 StudyFlow. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  )
}

function HomeContent() {
  return (
    <div>
      <h2>Welcome to StudyFlow</h2>
      <p>Organize your studies, track your progress, and achieve your goals.</p>
    </div>
  )
}

function CoursesContent() {
  return (
    <div>
      <h2>My Courses</h2>
      <p>Manage your courses and learning modules.</p>
    </div>
  )
}

function TasksContent() {
  return (
    <div>
      <h2>My Tasks</h2>
      <p>Track and complete your study tasks.</p>
    </div>
  )
}

export default App
