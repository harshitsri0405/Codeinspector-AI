import React, { useState } from 'react';
import API from '../services/api';

export default function CodeSubmit({ onUploadSuccess }) {
  const [uploadType, setUploadType] = useState('file'); // 'file' or 'snippet'
  const [projectName, setProjectName] = useState('');
  const [snippet, setSnippet] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      let response;
      if (uploadType === 'snippet') {
        response = await API.post('/code/submit', {
          project_name: projectName || 'Pasted Snippet Submission',
          snippet: snippet
        });
      } else {
        if (!file) {
          setMessage('Please select a file to upload first.');
          setLoading(false);
          return;
        }
        const formData = new FormData();
        formData.append('file', file);
        formData.append('project_name', projectName || file.name);

        response = await API.post('/code/submit', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      setMessage(`Success! Project ID: ${response.data.project_id}`);
      if (onUploadSuccess) onUploadSuccess(response.data.project_id);
    } catch (error) {
      setMessage(error.response?.data?.error || 'Submission failed. Make sure you are logged in.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 p-6 rounded-lg max-w-3xl mx-auto my-6">
      <h3 className="text-xl font-semibold mb-4 text-emerald-400">Submit Code for Review</h3>
      
      {/* Toggle Buttons */}
      <div className="flex space-x-4 mb-4">
        <button
          onClick={() => setUploadType('file')}
          className={`px-4 py-2 rounded font-medium transition ${uploadType === 'file' ? 'bg-emerald-500 text-gray-950' : 'bg-gray-700 text-gray-300'}`}
        >
          Upload Source File
        </button>
        <button
          onClick={() => setUploadType('snippet')}
          className={`px-4 py-2 rounded font-medium transition ${uploadType === 'snippet' ? 'bg-emerald-500 text-gray-950' : 'bg-gray-700 text-gray-300'}`}
        >
          Paste Code Snippet
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">Project Name (Optional)</label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="e.g., Auth Validation Service"
            className="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white focus:outline-none focus:border-emerald-500"
          />
        </div>

        {uploadType === 'file' ? (
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Choose File (.py, .js, .txt)</label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full bg-gray-900 text-gray-300 border border-gray-600 rounded p-2 file:bg-gray-700 file:border-none file:text-white file:px-3 file:py-1 file:rounded file:mr-3 file:cursor-pointer"
            />
          </div>
        ) : (
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Source Code Editor</label>
            <textarea
              rows="8"
              value={snippet}
              onChange={(e) => setSnippet(e.target.value)}
              placeholder="def my_function():\n    print('Hello World')"
              className="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white font-mono focus:outline-none focus:border-emerald-500"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-500 text-gray-950 font-bold py-2 rounded hover:bg-emerald-400 transition disabled:opacity-50"
        >
          {loading ? 'Processing Code Pipeline...' : 'Submit to Assistant'}
        </button>
      </form>

      {message && (
        <p className="mt-4 text-center text-sm font-semibold bg-gray-900 p-2 rounded border border-gray-700 text-amber-400">
          {message}
        </p>
      )}
    </div>
  );
}