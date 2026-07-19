import React from 'react';

export default function ReportDisplay({ reportData, metrics }) {
  if (!reportData) return null;

  return (
    <div className="max-w-4xl mx-auto my-8 space-y-6">
      {/* Overview Metric Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 border border-gray-700 p-6 rounded-lg text-center">
          <h4 className="text-sm text-gray-400 font-medium uppercase tracking-wider">Overall Quality Score</h4>
          <p className="text-4xl font-bold mt-2 text-emerald-400">{metrics?.overall_score ?? reportData.score} / 100</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 p-6 rounded-lg text-center">
          <h4 className="text-sm text-gray-400 font-medium uppercase tracking-wider">Cyclomatic Complexity</h4>
          <p className="text-4xl font-bold mt-2 text-amber-400">{metrics?.cyclomatic_complexity ?? '1.0'}</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 p-6 rounded-lg text-center">
          <h4 className="text-sm text-gray-400 font-medium uppercase tracking-wider">Maintainability Index</h4>
          <p className="text-4xl font-bold mt-2 text-sky-400">{metrics?.maintainability_index ?? '100'}</p>
        </div>
      </div>

      {/* Structural Extra Summary Info Dashboard */}
      {metrics && (
        <div className="bg-gray-800 border border-gray-700 p-4 rounded-lg flex justify-around text-sm text-gray-300">
          <div><span className="text-gray-500 font-semibold">Total Classes:</span> {metrics.classes_count}</div>
          <div><span className="text-gray-500 font-semibold">Total Functions:</span> {metrics.functions_count}</div>
        </div>
      )}

      {/* Detail Analysis Findings Table */}
      <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-700 bg-gray-850">
          <h3 className="text-lg font-semibold text-white">Detailed Code Review Findings</h3>
        </div>

        {reportData.findings?.length === 0 ? (
          <div className="p-6 text-center text-gray-400">🎉 Bravo! No significant structural issues or security vulnerabilities identified.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-gray-300">
              <thead className="bg-gray-900 text-gray-400 uppercase text-xs tracking-wider">
                <tr>
                  <th className="px-6 py-3">Severity</th>
                  <th className="px-6 py-3">Issue</th>
                  <th className="px-6 py-3">Location & Explanation</th>
                  <th className="px-6 py-3">Suggestion</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {reportData.findings.map((f, index) => (
                  <tr key={index} className="hover:bg-gray-750 transition">
                    <td className="px-6 py-4 vertical-align-top">
                      <span className={`px-2 py-1 text-xs rounded font-bold ${
                        f.severity === 'High' || f.severity === 'Critical' ? 'bg-red-900/40 text-red-400 border border-red-700' :
                        f.severity === 'Medium' ? 'bg-amber-900/40 text-amber-400 border border-amber-700' :
                        'bg-blue-900/40 text-blue-400 border border-blue-700'
                      }`}>
                        {f.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-semibold text-white">{f.issue}</td>
                    <td className="px-6 py-4">
                      <div className="text-xs text-gray-500 font-mono mb-1">File: {f.file_name} {f.line_number ? `| Line: ${f.line_number}` : ''}</div>
                      <div className="text-gray-300 font-mono text-xs max-w-md whitespace-pre-wrap">{f.explanation}</div>
                    </td>
                    <td className="px-6 py-4 text-gray-400 text-xs">{f.suggestion}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}