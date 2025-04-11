import React from 'react';

export default function DownloadReport({ outputPath }) {
  if (!outputPath) return null;

  // 🧠 Decide if the path is absolute (for Hugging Face /data) or local (static/reports)
  const isHosted = outputPath.startsWith("/data/");
  const filename = outputPath.split('/').pop();

  // 👇 Use either backend proxy download path (recommended for HF) or static path (local)
  const downloadUrl = isHosted
    ? `/download?path=${encodeURIComponent(outputPath)}` // Proxy route
    : `/static/reports/${filename}`; // Local dev

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