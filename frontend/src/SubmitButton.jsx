import React from 'react';

export default function SubmitButton({ onClick, disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="submit-btn"
    >
      Summarize PDFs
    </button>
  );
}