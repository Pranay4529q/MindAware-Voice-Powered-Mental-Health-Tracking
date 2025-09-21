import React from 'react';

const HistoryList = ({ history }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Date
            </th>
            <th className="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Result
            </th>
            <th className="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Confidence
            </th>
          </tr>
        </thead>
        <tbody>
          {history.map((record) => (
            <tr key={record.id}>
              <td className="py-2 px-4 border-b border-gray-200">
                {new Date(record.timestamp).toLocaleString()}
              </td>
              <td className="py-2 px-4 border-b border-gray-200">
                <span 
                  className={`px-2 py-1 rounded text-sm font-semibold ${
                    record.overall_class === 0 
                      ? 'bg-green-100 text-green-800' 
                      : record.overall_class === 1 
                      ? 'bg-yellow-100 text-yellow-800' 
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {record.class_label}
                </span>
              </td>
              <td className="py-2 px-4 border-b border-gray-200">
                {(record.confidence * 100).toFixed(1)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryList;