import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-blue-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-xl font-bold">
          Mental Health Audio Analyzer
        </Link>

        {user ? (
          <div className="flex items-center">
            <Link to="/" className="text-white hover:text-blue-200 px-3 py-2">
              Dashboard
            </Link>
            <Link
              to="/analyze"
              className="text-white hover:text-blue-200 px-3 py-2"
            >
              Analyze Audio
            </Link>
            <Link
              to="/profile"
              className="text-white hover:text-blue-200 px-3 py-2"
            >
              Profile
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded ml-4"
            >
              Logout
            </button>
          </div>
        ) : (
          <div>
            <Link
              to="/login"
              className="text-white hover:text-blue-200 px-3 py-2"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="bg-white hover:bg-gray-100 text-blue-600 font-bold py-1 px-3 rounded ml-2"
            >
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
