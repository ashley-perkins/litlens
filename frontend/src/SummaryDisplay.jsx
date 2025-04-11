import React from 'react';

export default function SummaryDisplay({ summaries }) {
  if (!summaries || summaries.length === 0) return null;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-2">Summaries</h2>
      {summaries.map((summary, index) => (
        <div key={index} className="mb-4 p-4 border border-gray-300 rounded">
          <pre className="whitespace-pre-wrap text-sm">{summary}</pre>
        </div>
      ))}
    </div>
  );
}