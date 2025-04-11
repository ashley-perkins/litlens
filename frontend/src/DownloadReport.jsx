import React from 'react';

export default function DownloadReport({ outputPath }) {
  if (!outputPath) return null;

  // Extract just the filename from the full path
  const filename = outputPath.split('/').pop();
  const downloadUrl = `/static/reports/${filename}`;

  return (
    <div className="mt-4">
      <a
        href={downloadUrl}
        download
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 inline-flex items-center"
      >
        <span role="img" aria-label="download">📥</span>&nbsp;Download Full Report
      </a>
    </div>
  );
}