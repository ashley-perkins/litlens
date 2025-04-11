import React from 'react';

export default function DownloadReport({ goal, summaries }) {
  if (!goal || !summaries || summaries.length === 0) return null;

  const handleDownload = async () => {
    try {
      const response = await fetch('/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ goal, summaries }),
      });

      if (!response.ok) {
        throw new Error(`Failed to generate report: ${response.statusText}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${goal}_summary_report.md`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('🛑 Error downloading report:', error);
      alert('Failed to download the report. Check the console for details.');
    }
  };

  return (
    <div className="mt-4">
      <button
        onClick={handleDownload}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 inline-flex items-center"
      >
        <span role="img" aria-label="download">📥</span>&nbsp;Download Full Report
      </button>
    </div>
  );
}