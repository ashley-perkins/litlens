import React from 'react';

export default function UploadArea({ onFileChange }) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700">Upload PDF(s)</label>
      <input
        type="file"
        accept=".pdf"
        multiple
        onChange={onFileChange}
        className="mt-1 block w-full"
      />
    </div>
  );
}