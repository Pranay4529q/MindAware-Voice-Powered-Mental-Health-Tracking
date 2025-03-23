import React from "react";
import AudioUploader from "./AudioUploader";
import ResultDisplay from "./ResultDisplay";

const AudioAnalysis = () => {
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [audioFile, setAudioFile] = React.useState(null);
  const [error, setError] = React.useState("");

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-4">
          Audio Mental Health Analysis
        </h1>
        <p className="mb-6">
          Upload an audio recording to analyze your mental health status. The
          system will process your audio and classify it into one of three
          categories based on emotional signals detected in your voice.
        </p>

        {!result && (
          <AudioUploader
            setResult={setResult}
            setLoading={setLoading}
            loading={loading}
            setAudioFile={setAudioFile}
            setError={setError}
          />
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4">
            {error}
          </div>
        )}

        {result && (
          <ResultDisplay
            result={result}
            audioFile={audioFile}
            onReset={() => {
              setResult(null);
              setAudioFile(null);
              setError("");
            }}
          />
        )}
      </div>
    </div>
  );
};

export default AudioAnalysis;
