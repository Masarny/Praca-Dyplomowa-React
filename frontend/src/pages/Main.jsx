import { Link } from "react-router-dom";

export default function Main() {
  return (
    <div className="container">
      <h1>Aplikacja Menedżer Haseł</h1>
      <div className="nav-container">
        <Link to="/guidelines" className="nav"><h2>Wytyczne</h2></Link>
        <Link to="/creator" className="nav"><h2>Kreator</h2></Link>
        <Link to="/tester" className="nav"><h2>Tester</h2></Link>
        <Link to="/user_passwords" className="nav"><h2>Hasła Użytkownika</h2></Link>
      </div>
    </div>
  );
}
