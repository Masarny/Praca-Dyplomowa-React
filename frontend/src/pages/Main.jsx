import { Link } from "react-router-dom";

export default function Main() {
  return (
    <div className="container">
      <h1>Password Manager Application</h1>
      <div className="nav-container">
        <Link to="/guidelines" className="nav"><h2>Guidelines</h2></Link>
        <Link to="/creator" className="nav"><h2>Creator</h2></Link>
        <Link to="/tester" className="nav"><h2>Tester</h2></Link>
        <Link to="/user_passwords" className="nav"><h2>User Passwords</h2></Link>
      </div>
    </div>
  );
}
