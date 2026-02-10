import { useState } from 'react';

export default function Courses() {
  const [courses, setCourses] = useState<Array<{ id: number; name: string; chapters: number }>>([
    { id: 1, name: 'Mathématiques', chapters: 5 },
    { id: 2, name: 'Français', chapters: 3 },
    { id: 3, name: 'Anglais', chapters: 4 },
  ]);

  return (
    <div className="page-courses">
      <h2>Mes cours</h2>
      <p>Gère tes cours et tes chapitres.</p>
      <div className="courses-list">
        {courses.map((course) => (
          <div key={course.id} className="course-card">
            <h3>{course.name}</h3>
            <p>{course.chapters} chapitres</p>
          </div>
        ))}
      </div>
    </div>
  );
}