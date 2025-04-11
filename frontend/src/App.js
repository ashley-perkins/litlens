import React, { useState } from 'react';
import UploadArea from './UploadArea';
import GoalInput from './GoalInput';
import SubmitButton from './SubmitButton';
import SummaryDisplay from './SummaryDisplay';

function App() {
  const [files, setFiles] = useState([]);
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFiles(Array.from(e.target.files));
  const handleGoalChange = (e) => setGoal(e.target.value);
  const [summaries, setSummaries] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setSummaries([]);
  
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    formData.append('goal', goal);
  
    try {
      const response = await fetch('https://ashley-perkins-litlens.hf.space/summarize-pdfs', {
        method: 'POST',
        body: formData,
      });
  
      console.log("Raw fetch response:", response);
  
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error response:", errorText);
        throw new Error('Failed to fetch summary.');
      }
  
      const result = await response.json();
      setSummaries(Array.isArray(result) ? result : [result]); // just in case
    } catch (err) {
      console.error("JS Fetch Error:", err);
      setError('Something went wrong while summarizing. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">LitLens</h1>
      <UploadArea onFileChange={handleFileChange} />
      <GoalInput goal={goal} onGoalChange={handleGoalChange} />
      <SubmitButton onClick={handleSubmit} disabled={loading || files.length === 0} />
  
      {loading && <p className="mt-4 text-blue-600">Summarizing… please wait ✨</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
  
      <SummaryDisplay summaries={summaries} />
    </div>
  );}

export default App;
