import * as React from 'react';

export default function Home() {
  return (
    <div className="page-home">
      <h2>Bienvenue sur StudyFlow</h2>
      <p>Organise tes cours, suis tes tâches, et avance proprement.</p>
      <div className="home-features">
        <div className="feature">
          <h3>📚 Gère tes cours</h3>
          <p>Organise tous tes cours par matière et par chapitre.</p>
        </div>
        <div className="feature">
          <h3>✅ Suis tes tâches</h3>
          <p>Crée et complète tes tâches d'étude facilement.</p>
        </div>
        <div className="feature">
          <h3>📊 Vois ta progression</h3>
          <p>Suivis ton avancement et célèbre tes progrès.</p>
        </div>
      </div>
    </div>
  );
}