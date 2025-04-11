import React, { useState } from 'react';
import UploadArea from './UploadArea';
import GoalInput from './GoalInput';
import SubmitButton from './SubmitButton';
import SummaryDisplay from './SummaryDisplay';
import DownloadReport from './DownloadReport';



function App() {
  const [files, setFiles] = useState([]);
  const [goal, setGoal] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFiles(Array.from(e.target.files));
  const handleGoalChange = (e) => setGoal(e.target.value);
  const [summaries, setSummaries] = useState([]);
  const [error, setError] = useState('');
  const [reportPath, setReportPath] = useState('');
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
      console.log("🧠 Summary API result:", result);
      setSummaries(result.summaries || []);
      setReportPath(result.output_path || '')
    } catch (err) {
      console.error("JS Fetch Error:", err);
      setError('Something went wrong while summarizing. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="container">
        <h1 className="title">LitLens</h1>
        <UploadArea onFileChange={handleFileChange} />
        <GoalInput goal={goal} onGoalChange={handleGoalChange} />
        <SubmitButton onClick={handleSubmit} disabled={loading || files.length === 0} />
  
        {loading && (
          <p className="status loading">
            <span className="spinner" /> Summarizing... please wait
          </p>
        )}
  
        {error && <p className="status error">{error}</p>}
  
        <SummaryDisplay summaries={summaries} />
        {reportPath && <DownloadReport goal={goal} summaries={summaries} />}
      </div>
  
      <footer className="footer">
        <p>Built by Ashley Perkins · LitLens v1.0 · 2025</p>
      </footer>
    </>
  );}
export default App;
