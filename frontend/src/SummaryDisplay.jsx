import React from 'react';

export default function SummaryDisplay({ summaries }) {
  if (!summaries || summaries.length === 0) return null;

  return (
    <div className="summary-section">
    <h2>Summaries</h2>
    {summaries.map((summaryObj, index) => (
        <div key={index} className="summary-card">
        <h3 className="summary-title">
            {summaryObj.title || summaryObj.filename}
        </h3>
        <pre className="summary-body">{summaryObj.summary}</pre>
        </div>
    ))}
    </div>
  );
}