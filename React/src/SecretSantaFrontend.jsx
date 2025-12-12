import React, { useState } from 'react';
import { Upload, Download, Users, Gift, AlertCircle, CheckCircle, Server, FileText, Loader } from 'lucide-react';

const SecretSantaFrontend = () => {
  const [apiUrl, setApiUrl] = useState('http://localhost:8000');
  const [currentEmployeesFile, setCurrentEmployeesFile] = useState(null);
  const [previousAssignmentsFile, setPreviousAssignmentsFile] = useState(null);
  const [jsonEmployees, setJsonEmployees] = useState('');
  const [jsonPreviousAssignments, setJsonPreviousAssignments] = useState('');
  const [mode, setMode] = useState('csv'); // 'csv' or 'json'
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState(null);

  // Check API health
  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${apiUrl}/health`);
      if (response.ok) {
        setApiStatus('healthy');
        setError('');
        return true;
      } else {
        setApiStatus('error');
        return false;
      }
    } catch (err) {
      setApiStatus('error');
      setError(`Cannot connect to API at ${apiUrl}. Make sure the FastAPI server is running.`);
      return false;
    }
  };

  // Handle CSV file upload
  const handleFileUpload = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      if (type === 'employees') {
        setCurrentEmployeesFile(file);
      } else {
        setPreviousAssignmentsFile(file);
      }
    }
  };

  // Submit CSV files
  const submitCSV = async () => {
    if (!currentEmployeesFile) {
      setError('Please upload the current employees CSV file');
      return;
    }

    setError('');
    setResults(null);
    setLoading(true);

    const isHealthy = await checkApiHealth();
    if (!isHealthy) {
      setLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append('employees_file', currentEmployeesFile);
      if (previousAssignmentsFile) {
        formData.append('previous_assignments_file', previousAssignmentsFile);
      }

      const response = await fetch(`${apiUrl}/assign/csv`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMsg = 'Failed to generate assignments';
        try {
          const errorData = await response.json();
          errorMsg = errorData.detail || JSON.stringify(errorData);
        } catch {}
        throw new Error(errorMsg);
      }

      // Get the CSV content
      const csvBlob = await response.blob();
      const csvText = await csvBlob.text();

      // Parse CSV to display
      const lines = csvText.trim().split('\n');
      const assignments = [];

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        assignments.push({
          employee_name: values[0] || '',
          employee_email: values[1] || '',
          secret_child_name: values[2] || '',
          secret_child_email: values[3] || ''
        });
      }

      setResults({
        assignments,
        csvContent: csvText,
        totalAssignments: assignments.length
      });

    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  // Submit JSON data
  const submitJSON = async () => {
    if (!jsonEmployees.trim()) {
      setError('Please enter employee data in JSON format');
      return;
    }

    setError('');
    setResults(null);
    setLoading(true);

    const isHealthy = await checkApiHealth();
    if (!isHealthy) {
      setLoading(false);
      return;
    }

    try {
      const employeesData = JSON.parse(jsonEmployees);
      let previousData = null;

      if (jsonPreviousAssignments.trim()) {
        previousData = JSON.parse(jsonPreviousAssignments);
      }

      const payload = {
        current_employees: employeesData,
        previous_assignments: previousData
      };

      const response = await fetch(`${apiUrl}/assign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let errMsg = 'Failed to generate assignments';
        try {
          const errData = await response.json();
          errMsg = errData.detail || JSON.stringify(errData);
        } catch {}
        throw new Error(errMsg);
      }

      const data = await response.json();

      // Convert to CSV format for consistency
      const csvLines = ['Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID'];
      data.assignments.forEach(a => {
        csvLines.push(`${a.employee_name},${a.employee_email},${a.secret_child_name},${a.secret_child_email}`);
      });
      const csvContent = csvLines.join('\\n');

      setResults({
        assignments: data.assignments,
        csvContent,
        totalAssignments: data.total_assignments
      });

    } catch (err) {
      if (err instanceof SyntaxError) {
        setError('Invalid JSON format. Please check your input.');
      } else {
        setError(err.message || String(err));
      }
    } finally {
      setLoading(false);
    }
  };

  // Download CSV
  const downloadCSV = () => {
    if (!results) return;

    const blob = new Blob([results.csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'secret_santa_assignments.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  // Load sample JSON data
  const loadSampleJSON = () => {
    const sampleEmployees = [
      { "name": "Hamish Murray", "email": "hamish.murray@acme.com" },
      { "name": "Layla Graham", "email": "layla.graham@acme.com" },
      { "name": "Matthew King", "email": "matthew.king@acme.com" },
      { "name": "Benjamin Collins", "email": "benjamin.collins@acme.com" },
      { "name": "Isabella Scott", "email": "isabella.scott@acme.com" }
    ];
    setJsonEmployees(JSON.stringify(sampleEmployees, null, 2));
    setJsonPreviousAssignments('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-green-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Gift className="text-red-600" size={48} />
            <h1 className="text-4xl font-bold text-gray-800">Secret Santa System</h1>
          </div>
          <p className="text-gray-600 mb-4">Powered by DigitalXC</p>

          {/* API URL Configuration
          <div className="flex items-center justify-center gap-3 max-w-md mx-auto">
            <Server className="text-blue-600" size={20} />
            <input
              type="text"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm"
              placeholder="API URL"
            />
            <button
              onClick={checkApiHealth}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
            >
              Test
            </button>
          </div> */}

          {apiStatus && (
            <div className={`mt-2 text-sm ${apiStatus === 'healthy' ? 'text-green-600' : 'text-red-600'}`}>
              {apiStatus === 'healthy' ? '✓ API Connected' : '✗ API Unavailable'}
            </div>
          )}
        </div>

        {/* Mode Selection */}
        <div className="flex justify-center gap-4 mb-6">
          <button
            onClick={() => setMode('csv')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              mode === 'csv'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-center gap-2">
              <FileText size={20} />
              CSV Upload
            </div>
          </button>
          <button
            onClick={() => setMode('json')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              mode === 'json'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-center gap-2">
              <Users size={20} />
              JSON Input
            </div>
          </button>
        </div>

        {/* CSV Mode */}
        {mode === 'csv' && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-6">Upload CSV Files</h2>

            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Current Employees */}
              <div>
                <label className="flex items-center gap-2 mb-3 font-semibold text-gray-700">
                  <Users className="text-blue-600" size={20} />
                  Current Employees CSV (Required)
                </label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => handleFileUpload(e, 'employees')}
                  className="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 transition-colors cursor-pointer"
                />
                {currentEmployeesFile && (
                  <p className="mt-2 text-sm text-green-600">✓ {currentEmployeesFile.name}</p>
                )}
                <p className="mt-2 text-sm text-gray-500">
                  Format: Employee_Name, Employee_EmailID
                </p>
              </div>

              {/* Previous Assignments */}
              <div>
                <label className="flex items-center gap-2 mb-3 font-semibold text-gray-700">
                  <Upload className="text-purple-600" size={20} />
                  Previous Assignments CSV (Optional)
                </label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => handleFileUpload(e, 'previous')}
                  className="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-500 transition-colors cursor-pointer"
                />
                {previousAssignmentsFile && (
                  <p className="mt-2 text-sm text-green-600">✓ {previousAssignmentsFile.name}</p>
                )}
                <p className="mt-2 text-sm text-gray-500">
                  Format: Employee_Name, Employee_EmailID, Secret_Child_Name, Secret_Child_EmailID
                </p>
              </div>
            </div>

            <button
              onClick={submitCSV}
              disabled={loading || !currentEmployeesFile}
              className="w-full bg-gradient-to-r from-red-600 to-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-red-700 hover:to-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <Loader className="animate-spin" size={20} />
                  Generating...
                </div>
              ) : (
                'Generate Assignments'
              )}
            </button>
          </div>
        )}

        {/* JSON Mode */}
        {mode === 'json' && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-6">Enter JSON Data</h2>

            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Current Employees JSON */}
              <div>
                <label className="flex items-center gap-2 mb-3 font-semibold text-gray-700">
                  <Users className="text-blue-600" size={20} />
                  Current Employees (Required)
                </label>
                <textarea
                  value={jsonEmployees}
                  onChange={(e) => setJsonEmployees(e.target.value)}
                  className="w-full h-64 p-3 border border-gray-300 rounded-lg font-mono text-sm"
                  placeholder='[
  {"name": "John Doe", "email": "john@acme.com"},
  {"name": "Jane Smith", "email": "jane@acme.com"}
]'
                />
                <button
                  onClick={loadSampleJSON}
                  className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                  Load Sample Data
                </button>
              </div>

              {/* Previous Assignments JSON */}
              <div>
                <label className="flex items-center gap-2 mb-3 font-semibold text-gray-700">
                  <Upload className="text-purple-600" size={20} />
                  Previous Assignments (Optional)
                </label>
                <textarea
                  value={jsonPreviousAssignments}
                  onChange={(e) => setJsonPreviousAssignments(e.target.value)}
                  className="w-full h-64 p-3 border border-gray-300 rounded-lg font-mono text-sm"
                  placeholder='[
  {
    "employee_name": "John Doe",
    "employee_email": "john@acme.com",
    "secret_child_name": "Jane Smith",
    "secret_child_email": "jane@acme.com"
  }
]'
                />
              </div>
            </div>

            <button
              onClick={submitJSON}
              disabled={loading || !jsonEmployees.trim()}
              className="w-full bg-gradient-to-r from-red-600 to-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-red-700 hover:to-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <Loader className="animate-spin" size={20} />
                  Generating...
                </div>
              ) : (
                'Generate Assignments'
              )}
            </button>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="text-red-600 flex-shrink-0" size={24} />
              <div>
                <h3 className="font-semibold text-red-800 mb-1">Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {results && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <CheckCircle className="text-green-600" size={24} />
                <h2 className="text-xl font-semibold">Assignments Generated Successfully!</h2>
              </div>
              <button
                onClick={downloadCSV}
                className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Download size={20} />
                Download CSV
              </button>
            </div>

            <p className="text-gray-600 mb-4">Total assignments: {results.totalAssignments}</p>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gradient-to-r from-red-100 to-green-100">
                    <th className="border border-gray-300 px-4 py-2 text-left">Employee Name</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Employee Email</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Secret Child Name</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Secret Child Email</th>
                  </tr>
                </thead>
                <tbody>
                  {results.assignments.map((assignment, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-2">{assignment.employee_name}</td>
                      <td className="border border-gray-300 px-4 py-2 text-sm text-gray-600">
                        {assignment.employee_email}
                      </td>
                      <td className="border border-gray-300 px-4 py-2 font-semibold text-green-700">
                        {assignment.secret_child_name}
                      </td>
                      <td className="border border-gray-300 px-4 py-2 text-sm text-gray-600">
                        {assignment.secret_child_email}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* API Documentation */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-3">Backend API Endpoints:</h3>
          <ul className="space-y-2 text-blue-800 text-sm">
            <li><code className="bg-blue-100 px-2 py-1 rounded">POST {apiUrl}/assign</code> - JSON-based assignments</li>
            <li><code className="bg-blue-100 px-2 py-1 rounded">POST {apiUrl}/assign/csv</code> - CSV file upload</li>
            <li><code className="bg-blue-100 px-2 py-1 rounded">GET {apiUrl}/health</code> - Health check</li>
            <li><code className="bg-blue-100 px-2 py-1 rounded">GET {apiUrl}/docs</code> - Interactive API docs (Swagger UI)</li>
          </ul>

          <div className="mt-4 pt-4 border-t border-blue-200">
            <h4 className="font-semibold text-blue-900 mb-2">Quick Start:</h4>
            <ol className="space-y-1 text-blue-800 text-sm list-decimal list-inside">
              <li>Start FastAPI: <code className="bg-blue-100 px-2 py-1 rounded">uvicorn main:app --reload</code></li>
              <li>Test API connection using the "Test" button above</li>
              <li>Choose CSV upload or JSON input mode</li>
              <li>Generate and download your Secret Santa assignments!</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecretSantaFrontend;
