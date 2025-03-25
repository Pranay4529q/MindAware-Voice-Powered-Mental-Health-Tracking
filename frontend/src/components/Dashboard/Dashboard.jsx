import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import HistoryList from "../Dashboard/HistoryList";

const Dashboard = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { token } = useContext(AuthContext);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const base_url = process.env.REACT_APP_API_URL;
        const response = await fetch(`${base_url}/api/history`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch history");
        }

        const data = await response.json();
        setHistory(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [token]);

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h1 className="text-2xl font-bold mb-4">Mental Health Dashboard</h1>
        <p className="mb-4">
          Welcome to your mental health audio analysis dashboard. Here you can
          track your mental health status over time based on audio analysis.
        </p>
        <Link
          to="/analyze"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Analyze New Audio
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Your Recent History</h2>

        {loading ? (
          <p>Loading history...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : history.length === 0 ? (
          <p>No records found. Start by analyzing your first audio file.</p>
        ) : (
          <HistoryList history={history} />
        )}
      </div>
    </div>
  );
};

export default Dashboard;
