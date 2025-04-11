import React from 'react';

export default function GoalInput({ goal, onGoalChange }) {
  return (
    <div className="mb-4">
      <label className="label">Research Goal (Optional)</label>
      <input
        type="text"
        value={goal}
        onChange={onGoalChange}
        placeholder="e.g., Identify key biomarkers for lung cancer"
        className="text-input"
      />
    </div>
  );
}