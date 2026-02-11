import { useState } from "react";
import client from "../api/client";
import { useNavigate } from "react-router-dom";


interface LoginResponse {
  access_token: string;
}

export default function Login() {
  const [email, setEmail] = useState("test@test.com");
  const [password, setPassword] = useState("123456");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();


  const handleLogin = async () => {
    try {
      const res = await client.post<LoginResponse>("/api/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", res.data.access_token);
      setMsg("✅ Connecté !");
      navigate("/");
    } catch (err) {
      console.error(err);
      setMsg("❌ Erreur login");
    }
  };

  const testBackend = async () => {
    try {
      const res = await client.get("/health");
      console.log("BACKEND OK:", res.data);
      setMsg("✅ Backend accessible");
    } catch (err) {
      console.error(err);
      setMsg("❌ Erreur backend");
    }
  };

  return (
    <div className="card">
      <h2>Connexion</h2>

      <div className="form">
        <div>
          <div className="label">Email</div>
          <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>

        <div>
          <div className="label">Mot de passe</div>
          <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>

        <div className="row">
          <button className="btn" onClick={handleLogin}>Se connecter</button>
        </div>

        <div className="msg">{msg}</div>
      </div>
    </div>
  );

}
