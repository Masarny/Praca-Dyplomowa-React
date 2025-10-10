import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Main from "./pages/main";
import Creator from "./pages/Creator";
import Tester from "./pages/Tester";
import Guidelines from "./pages/Guidelines";
import Login from "./pages/Login";
import UserPasswords from "./pages/UserPasswords";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/main" element={<Main />} />
        <Route path="/creator" element={<Creator />} />
        <Route path="/tester" element={<Tester />} />
        <Route path="/guidelines" element={<Guidelines />} />
        <Route path="/login" element={<Login />} />
        <Route path="/user_passwords" element={<UserPasswords />} />
      </Routes>
    </Router>
  );
}
