import { Link } from "react-router-dom";

export default function UserPasswords() {
  const passwords = [
    { site: "gmail.com", username: "user1", password: "********" },
    { site: "facebook.com", username: "user2", password: "********" },
  ];

  return (
    <div className="container">
      <h2>User Passwords</h2>
      <table>
        <thead>
          <tr>
            <th>Site</th>
            <th>Username</th>
            <th>Password</th>
          </tr>
        </thead>
        <tbody>
          {passwords.map((p, i) => (
            <tr key={i}>
              <td>{p.site}</td>
              <td>{p.username}</td>
              <td>{p.password}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <Link to="/main"><button className="btn">Return</button></Link>
    </div>
  );
}
