import React from 'react';

export default function SummaryDisplay({ summaries }) {
  if (!summaries || summaries.length === 0) return null;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-4">Summaries</h2>
      {summaries.map((summaryObj, index) => (
        <div key={index} className="mb-6 p-4 border border-gray-300 rounded shadow-sm">
          <h3 className="text-lg font-bold text-blue-700 mb-2">
            {summaryObj.title || summaryObj.filename}
          </h3>
          <pre className="whitespace-pre-wrap text-sm leading-relaxed">
            {summaryObj.summary}
          </pre>
        </div>
      ))}
    </div>
  );
}