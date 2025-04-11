import React from 'react';

export default function UploadArea({ onFileChange }) {
  return (
    <div className="section">
        <label className="label">Upload PDF(s)</label>
        <input
            type="file"
            accept=".pdf"
            multiple
            onChange={onFileChange}
            className="input-file"
        />
    </div>
  );
}