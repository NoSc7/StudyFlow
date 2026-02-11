import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect } from "react";
import "../App.css";
import Login from "./Login";
import Courses from "./Courses";



/* ---------- Pages ---------- */

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

function HeaderRight() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("access_token");

  const isOnLogin = location.pathname === "/login";

  const handleClick = () => {
    if (token) {
      localStorage.removeItem("access_token");
      navigate("/login");
    } else {
      navigate("/login");
    }
  };

  return (
    <button className="header-btn" onClick={handleClick} disabled={!token && isOnLogin}>
      {token ? "Logout" : "Login"}
    </button>
  );
}


/* ---------- App ---------- */

export default function App() {

  // ✅ Hook BIEN placé (dans le composant)
  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((res) => res.json())
      .then((data) => console.log("BACKEND:", data))
      .catch((err) => console.error("ERREUR:", err));
  }, []);

  return (
    <Router>
      <div className="app">

        <header className="app-header">
          <div className="header-inner">
            <div>
              <h1>StudyFlow</h1>
              <p>Ton assistant d’organisation</p>
            </div>

            <HeaderRight />
          </div>
        </header>


        <nav className="app-nav">
          <ul>
            <li><Link to="/">Accueil</Link></li>
            <li><Link to="/courses">Cours</Link></li>
            <li><Link to="/tasks">Tâches</Link></li>
            <li><Link to="/profile">Profil</Link></li>
          </ul>
        </nav>

        <main className="app-main">
          <div className="page">
            <Routes>
              <Route path="/" element={<HomeContent />} />
              <Route path="/courses" element={<Courses />} />
              <Route path="/tasks" element={<TasksContent />} />
              <Route path="/profile" element={<ProfileContent />} />
              <Route path="*" element={<NotFound />} />
              <Route path="/login" element={<Login />} />
            </Routes>
          </div>
        </main>


        <footer className="app-footer">
          <p>&copy; 2026 StudyFlow. Tous droits réservés.</p>
        </footer>

      </div>
    </Router>
  );
}
