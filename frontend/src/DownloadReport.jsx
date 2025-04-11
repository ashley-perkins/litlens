import React from 'react';

export default function DownloadReport({ outputPath }) {
  if (!outputPath) return null;

  return (
    <div className="mt-4">
      <a
        href={outputPath}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 inline-flex items-center"
      >
        <span role="img" aria-label="download">📥</span>&nbsp;Download Full Report
      </a>
    </div>
  );
}