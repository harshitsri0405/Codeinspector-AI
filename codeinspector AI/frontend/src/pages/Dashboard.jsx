import React, { useState } from 'react';
import CodeSubmit from '../components/CodeSubmit';
import ReportDisplay from '../components/ReportDisplay';
import API from '../services/api';

export default function Dashboard() {
  const [report, setReport] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUploadSuccess = async (projectId) => {
    setLoading(true);
    setReport(null);
    setMetrics(null);

    try {
      // 1. Trigger Multi-Stage Static Scanner (Day 5 & Day 6 modules)
      const analyzeRes = await API.post(`/review/analyze/${projectId}`);
      setMetrics(analyzeRes.data.metrics);

      // 2. Fetch full structured details from data rows
      const reportRes = await API.get(`/review/report/${analyzeRes.data.review_id}`);
      setReport(reportRes.data);
    } catch (error) {
      alert("Analysis pipeline failed. Make sure to sign-in or check server status logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center border-b border-gray-700 pb-4 mb-8">
          <div>
            <h1 className="text-4xl font-bold text-emerald-400">AI Code Review Assistant</h1>
            <p className="text-gray-400 mt-1">Automated static code diagnostics and metric assessments.</p>
          </div>
          <div className="bg-gray-800 border border-gray-700 px-4 py-2 rounded text-sm text-gray-300 font-mono">
            {loading ? 'Pipeline Processing...' : 'Status: Ready'}
          </div>
        </header>

        <main className="space-y-8">
          {/* Submission Layer Component */}
          <CodeSubmit onUploadSuccess={handleUploadSuccess} />

          {/* Loading Loader Animation */}
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-400 mx-auto"></div>
              <p className="text-gray-400 mt-4 font-medium">Running static analysis scanners (Pylint, Bandit, Radon)...</p>
            </div>
          )}

          {/* Dynamic Analysis Report View Components Card */}
          <ReportDisplay reportData={report} metrics={metrics} />
        </main>
      </div>
    </div>
  );
}