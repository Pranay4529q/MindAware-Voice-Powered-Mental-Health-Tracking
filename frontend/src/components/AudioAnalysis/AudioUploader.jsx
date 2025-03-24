import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const AudioUploader = ({
  setResult,
  setLoading,
  loading,
  setAudioFile,
  setError,
}) => {
  const [selectedFile, setSelectedFile] = React.useState(null);
  const { token } = useContext(AuthContext);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select an audio file first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("audio", selectedFile);

      const response = await fetch("https://mindaware-backend.onrender.com/api/predict", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to analyze audio");
      }

      const data = await response.json();
      setResult(data);
      setAudioFile(selectedFile);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6">
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">
          Upload Audio File
        </label>
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
          className="w-full text-sm text-gray-700 p-2 border border-gray-300 rounded"
        />
        <p className="text-sm text-gray-500 mt-1">
          Supported formats: WAV, MP3, M4A
        </p>
      </div>

      <button
        onClick={handleUpload}
        disabled={loading || !selectedFile}
        className={`${
          loading || !selectedFile
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-700"
        } text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline`}
      >
        {loading ? (
          <div className="flex items-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Processing Audio...
          </div>
        ) : (
          "Analyze Audio"
        )}
      </button>
    </div>
  );
};

export default AudioUploader;
