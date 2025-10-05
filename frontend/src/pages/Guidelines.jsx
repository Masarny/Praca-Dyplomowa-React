import { Link } from "react-router-dom";

export default function Guidelines() {
  return (
    <div className="container">
      <h2>Guidelines</h2>
      <p>
        Tu możesz wstawić zasady tworzenia bezpiecznych haseł:
        - minimum 12 znaków,
        - różne typy znaków,
        - nie używaj tego samego hasła w wielu serwisach.
      </p>

      <Link to="/main"><button className="btn">Return</button></Link>
    </div>
  );
}
