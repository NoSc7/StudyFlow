export default function Profile() {
  const user = {
    name: 'Jean Dupont',
    email: 'jean@example.com',
    joinDate: '2026-01-15',
    courses: 3,
    tasks: 8,
  };

  return (
    <div className="page-profile">
      <h2>Mon profil</h2>
      <div className="profile-card">
        <div className="profile-info">
          <h3>{user.name}</h3>
          <p>Email: {user.email}</p>
          <p>Membre depuis: {user.joinDate}</p>
        </div>
        <div className="profile-stats">
          <div className="stat">
            <p className="stat-value">{user.courses}</p>
            <p className="stat-label">Cours</p>
          </div>
          <div className="stat">
            <p className="stat-value">{user.tasks}</p>
            <p className="stat-label">Tâches</p>
          </div>
        </div>
      </div>
    </div>
  );
}