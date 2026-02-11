import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../api/client";

type Course = {
  id: number;
  title: string;
  description?: string | null;
};

export default function Courses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [msg, setMsg] = useState("");

  const loadCourses = async () => {
    try {
      const res = await client.get<Course[]>("/api/courses");
      setCourses(res.data);
    } catch (err) {
      console.error(err);
      setMsg("❌ Impossible de charger les cours (console).");
    }
  };

  useEffect(() => {
    loadCourses();
  }, []);

  const addCourse = async () => {
    if (!title.trim()) {
      setMsg("⚠️ Mets un titre.");
      return;
    }

    try {
      setMsg("");
      await client.post("/api/courses", {
        title: title.trim(),
        description: description.trim() || null,
      });

      setTitle("");
      setDescription("");
      setMsg("✅ Cours ajouté !");
      loadCourses();
    } catch (err) {
      console.error(err);
      setMsg("❌ Erreur ajout (console).");
    }
  };

  return (
    <div className="page">
      <h2>Mes cours</h2>

      <div className="card">
        <h3>Ajouter un cours</h3>

        <input
          placeholder="Titre du cours"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          placeholder="Description (optionnel)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />

        <button onClick={addCourse}>Ajouter</button>
        {msg && <p className="msg">{msg}</p>}
      </div>

      <div className="card">
        <h3>Liste</h3>

        {courses.length === 0 ? (
          <p>Aucun cours pour l’instant.</p>
        ) : (
          <ul className="list">
            {courses.map((c) => (
              <li key={c.id}>
                <Link to={`/courses/${c.id}`}>{c.title}</Link>
                {c.description ? <small>{c.description}</small> : null}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
