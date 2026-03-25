import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div className="navbar">
      <h2> Scripture AI</h2>

      <div className="nav-links">
        <Link to="/">Upload</Link>
        <Link to="/chat">Chat</Link>
      </div>
    </div>
  );
}

export default Navbar;