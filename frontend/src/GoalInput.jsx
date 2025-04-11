import React from 'react';

export default function GoalInput({ goal, onGoalChange }) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700">Research Goal (Optional)</label>
      <input
        type="text"
        value={goal}
        onChange={onGoalChange}
        placeholder="e.g., Identify key biomarkers for lung cancer"
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
      />
    </div>
  );
}