import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Main from "./pages/main";
import Creator from "./pages/Creator";
import Tester from "./pages/Tester";
import Guidelines from "./pages/Guidelines";
import Login1 from "./pages/Login1";
import Login2 from "./pages/Login2";
import UserPasswords from "./pages/UserPasswords";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login1 />} />
        <Route path="/main" element={<Main />} />
        <Route path="/creator" element={<Creator />} />
        <Route path="/tester" element={<Tester />} />
        <Route path="/guidelines" element={<Guidelines />} />
        <Route path="/login_1" element={<Login1 />} />
        <Route path="/login_2" element={<Login2 />} />
        <Route path="/user_passwords" element={<UserPasswords />} />
      </Routes>
    </Router>
  );
}
