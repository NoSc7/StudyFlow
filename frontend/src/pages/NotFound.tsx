import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="page-not-found">
      <h2>404 - Page introuvable</h2>
      <p>Désolé, cette page n'existe pas.</p>
      <Link to="/" className="back-link">
        ← Retour à l'accueil
      </Link>
    </div>
  );
}