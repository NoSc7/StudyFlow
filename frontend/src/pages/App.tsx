import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "../App.css";

function HomeContent() {
  return (
    <div>
      <h2>Bienvenue sur StudyFlow</h2>
      <p>Organise tes cours, suis tes tâches, et avance proprement.</p>
    </div>
  );
}

function CoursesContent() {
  return (
    <div>
      <h2>Mes cours</h2>
      <p>Gère tes cours et tes chapitres.</p>
    </div>
  );
}

function TasksContent() {
  return (
    <div>
      <h2>Mes tâches</h2>
      <p>Suis et valide tes tâches d’étude.</p>
    </div>
  );
}

function ProfileContent() {
  return (
    <div>
      <h2>Profil</h2>
      <p>Paramètres et infos du compte (à venir).</p>
    </div>
  );
}

function NotFound() {
  return (
    <div>
      <h2>Page introuvable</h2>
      <p>Cette page n’existe pas.</p>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>StudyFlow</h1>
          <p>Ton assistant d’organisation</p>
        </header>

        <nav className="app-nav">
          <ul>
            <li>
              <Link to="/">Accueil</Link>
            </li>
            <li>
              <Link to="/courses">Cours</Link>
            </li>
            <li>
              <Link to="/tasks">Tâches</Link>
            </li>
            <li>
              <Link to="/profile">Profil</Link>
            </li>
          </ul>
        </nav>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomeContent />} />
            <Route path="/courses" element={<CoursesContent />} />
            <Route path="/tasks" element={<TasksContent />} />
            <Route path="/profile" element={<ProfileContent />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>&copy; 2026 StudyFlow. Tous droits réservés.</p>
        </footer>
      </div>
    </Router>
  );
}
