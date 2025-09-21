// import React, { useState } from "react";

// const ResultDisplay = ({ result, audioFile, onReset }) => {
//   const [showSegments, setShowSegments] = useState(false);

//   const getClassColor = (classIndex) => {
//     switch (classIndex) {
//       case 0:
//         return { bg: "bg-green-100", text: "text-green-800" };
//       case 1:
//         return { bg: "bg-yellow-100", text: "text-yellow-800" };
//       case 2:
//         return { bg: "bg-red-100", text: "text-red-800" };
//       default:
//         return { bg: "bg-gray-100", text: "text-gray-800" };
//     }
//   };

//   const getClassDescription = (classIndex) => {
//     switch (classIndex) {
//       case 0:
//         return "Your audio indicates a positive mental state with minimal signs of depression.";
//       case 1:
//         return "Your audio shows some moderate indicators that may be associated with mild depression.";
//       case 2:
//         return "Your audio displays several markers commonly associated with more severe depression.";
//       default:
//         return "Classification not available.";
//     }
//   };

//   return (
//     <div className="mt-6">
//       <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
//         <h2 className="text-xl font-bold mb-4">Analysis Results</h2>

//         <div className="mb-6">
//           <p className="mb-2">
//             <strong>Overall Assessment:</strong>
//           </p>
//           <div
//             className={`inline-block px-3 py-1 rounded-full ${
//               getClassColor(result.overall_prediction.predicted_class).bg
//             } ${
//               getClassColor(result.overall_prediction.predicted_class).text
//             } font-medium text-sm`}
//           >
//             {result.overall_prediction.class_label}
//           </div>
//           <p className="mt-2">
//             {getClassDescription(result.overall_prediction.predicted_class)}
//           </p>
//           <p className="mt-2">
//             <strong>Confidence:</strong>{" "}
//             {(result.overall_prediction.confidence * 100).toFixed(1)}%
//           </p>
//         </div>

//         <div className="mb-6">
//           <h3 className="font-bold mb-2">Probability Distribution:</h3>
//           {Object.entries(result.average_probabilities).map(
//             ([classLabel, prob]) => {
//               const percentage = (prob * 100).toFixed(1);
//               return (
//                 <div key={classLabel} className="mb-2">
//                   <div className="flex items-center">
//                     <span className="w-24">{classLabel}:</span>
//                     <div className="flex-1 bg-gray-200 rounded-full h-4">
//                       <div
//                         className="bg-blue-600 h-4 rounded-full"
//                         style={{ width: `${percentage}%` }}
//                       ></div>
//                     </div>
//                     <span className="ml-2 text-sm">{percentage}%</span>
//                   </div>
//                 </div>
//               );
//             }
//           )}
//         </div>

//         {audioFile && (
//           <div className="mb-6">
//             <h3 className="font-bold mb-2">Audio Sample:</h3>
//             <audio controls className="w-full">
//               <source
//                 src={URL.createObjectURL(audioFile)}
//                 type={audioFile.type}
//               />
//               Your browser does not support the audio element.
//             </audio>
//           </div>
//         )}

//         <div className="mb-6">
//           <button
//             onClick={() => setShowSegments(!showSegments)}
//             className="text-blue-600 hover:text-blue-800"
//           >
//             {showSegments ? "Hide" : "Show"} Detailed Segment Analysis ▼
//           </button>

//           {showSegments && (
//             <div className="mt-4 space-y-4">
//               {result.segment_predictions.map((segment) => (
//                 <div
//                   key={segment.segment}
//                   className="border border-gray-200 rounded p-4"
//                 >
//                   <p className="font-bold mb-2">
//                     Segment {segment.segment + 1}: {segment.class_label}
//                   </p>

//                   {Object.entries(segment.probabilities).map(
//                     ([classLabel, prob]) => {
//                       const percentage = (prob * 100).toFixed(1);
//                       return (
//                         <div key={classLabel} className="mb-1">
//                           <div className="flex items-center">
//                             <span className="w-24 text-sm">{classLabel}:</span>
//                             <div className="flex-1 bg-gray-200 rounded-full h-2">
//                               <div
//                                 className="bg-blue-400 h-2 rounded-full"
//                                 style={{ width: `${percentage}%` }}
//                               ></div>
//                             </div>
//                             <span className="ml-2 text-xs">{percentage}%</span>
//                           </div>
//                         </div>
//                       );
//                     }
//                   )}
//                 </div>
//               ))}
//             </div>
//           )}
//         </div>

//         <div className="flex justify-between">
//           <button
//             onClick={onReset}
//             className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
//           >
//             Analyze Another Recording
//           </button>

//           <button
//             onClick={() => window.print()}
//             className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
//           >
//             Save Results
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ResultDisplay;
import React, { useState } from "react";

const ResultDisplay = ({ result, audioFile, onReset }) => {
  const [showSegments, setShowSegments] = useState(false);

  const getClassColor = (classIndex) => {
    switch (classIndex) {
      case 0:
        return { bg: "bg-green-100", text: "text-green-800" };
      case 1:
        return { bg: "bg-yellow-100", text: "text-yellow-800" };
      case 2:
        return { bg: "bg-red-100", text: "text-red-800" };
      default:
        return { bg: "bg-gray-100", text: "text-gray-800" };
    }
  };

  const getClassDescription = (classIndex) => {
    switch (classIndex) {
      case 0:
        return "Your audio indicates a positive mental state with minimal signs of depression.";
      case 1:
        return "Your audio shows some moderate indicators that may be associated with mild depression.";
      case 2:
        return "Your audio displays several markers commonly associated with more severe depression.";
      default:
        return "Classification not available.";
    }
  };

  return (
    <div className="mt-6">
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h2 className="text-xl font-bold mb-4">Analysis Results</h2>

        <div className="mb-6">
          <p className="mb-2">
            <strong>Overall Assessment:</strong>
          </p>
          <div
            className={`inline-block px-3 py-1 rounded-full ${
              getClassColor(result.overall_prediction.predicted_class).bg
            } ${
              getClassColor(result.overall_prediction.predicted_class).text
            } font-medium text-sm`}
          >
            {result.overall_prediction.class_label}
          </div>
          <p className="mt-2">
            {getClassDescription(result.overall_prediction.predicted_class)}
          </p>
          <p className="mt-2">
            <strong>Confidence:</strong>{" "}
            {(result.overall_prediction.confidence * 100).toFixed(1)}%
          </p>
        </div>

        <div className="mb-6">
          <h3 className="font-bold mb-2">Probability Distribution:</h3>
          {Object.entries(result.average_probabilities).map(
            ([classLabel, prob]) => {
              const percentage = (prob * 100).toFixed(1);
              return (
                <div key={classLabel} className="mb-2">
                  <div className="flex items-center">
                    <span className="w-24">{classLabel}:</span>
                    <div className="flex-1 bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-blue-600 h-4 rounded-full"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm">{percentage}%</span>
                  </div>
                </div>
              );
            }
          )}
        </div>

        {audioFile && (
          <div className="mb-6">
            <h3 className="font-bold mb-2">Audio Sample:</h3>
            <audio controls className="w-full">
              <source
                src={URL.createObjectURL(audioFile)}
                type={audioFile.type}
              />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}

        <div className="mb-6">
          <button
            onClick={() => setShowSegments(!showSegments)}
            className="text-blue-600 hover:text-blue-800"
          >
            {showSegments ? "Hide" : "Show"} Detailed Segment Analysis ▼
          </button>

          {showSegments && (
            <div className="mt-4 space-y-4">
              {result.segment_predictions ? (
                result.segment_predictions.map((segment) => (
                  <div
                    key={segment.segment}
                    className="border border-gray-200 rounded p-4"
                  >
                    <p className="font-bold mb-2">
                      Segment {segment.segment + 1}: {segment.class_label}
                    </p>

                    {Object.entries(segment.probabilities).map(
                      ([classLabel, prob]) => {
                        const percentage = (prob * 100).toFixed(1);
                        return (
                          <div key={classLabel} className="mb-1">
                            <div className="flex items-center">
                              <span className="w-24 text-sm">
                                {classLabel}:
                              </span>
                              <div className="flex-1 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-blue-400 h-2 rounded-full"
                                  style={{ width: `${percentage}%` }}
                                ></div>
                              </div>
                              <span className="ml-2 text-xs">
                                {percentage}%
                              </span>
                            </div>
                          </div>
                        );
                      }
                    )}
                  </div>
                ))
              ) : (
                <p className="text-gray-600">
                  Segment analysis is not available for this recording.
                </p>
              )}
            </div>
          )}
        </div>

        <div className="flex justify-between">
          <button
            onClick={onReset}
            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Analyze Another Recording
          </button>

          <button
            onClick={() => window.print()}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Save Results
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;