import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div className="navbar">

      {/* LEFT → Upload */}
      <div className="nav-left">
        <Link to="/"> Upload</Link>
      </div>

      {/* CENTER */}
      <div className="nav-center">
        🕉️ Welcome to Scriptures AI
      </div>

      {/* RIGHT → Query */}
      <div className="nav-right">
        <Link to="/Chat"> Query</Link>
      </div>

    </div>
  );
}

export default Navbar;
