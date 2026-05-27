import { useState } from 'react'

const FILE_FIELDS = [
  { key: 'first_names', label: 'First Names', hint: 'first_names.txt — one name per line', accept: '.txt' },
  { key: 'last_names', label: 'Last Names', hint: 'last_names.txt — one name per line', accept: '.txt' },
  { key: 'employee_data', label: 'Employee Data', hint: 'employee_data.csv — with headers: job_title, country, salary, doj, dob', accept: '.csv' },
]

export default function ImportModal({ onClose, onImported }) {
  const [files, setFiles] = useState({ first_names: null, last_names: null, employee_data: null })
  const [importing, setImporting] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFile = (key, file) => {
    setFiles((prev) => ({ ...prev, [key]: file }))
    setResult(null)
    setError(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('first_names', files.first_names)
    formData.append('last_names', files.last_names)
    formData.append('employee_data', files.employee_data)

    setImporting(true)
    try {
      const res = await fetch('/api/employees/import', { method: 'POST', body: formData })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || res.statusText)
      setResult(data.imported)
      onImported()
    } catch (err) {
      setError(err.message)
    } finally {
      setImporting(false)
    }
  }

  const allSelected = files.first_names && files.last_names && files.employee_data

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-lg"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h2 className="text-base font-semibold text-gray-900 dark:text-white">Import Employees</h2>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Upload 3 files — line counts must match</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-4">
          {FILE_FIELDS.map((field) => (
            <div key={field.key}>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {field.label}
              </label>
              <input
                type="file"
                accept={field.accept}
                required
                onChange={(e) => handleFile(field.key, e.target.files[0] || null)}
                className="block w-full text-sm text-gray-600 dark:text-gray-400
                  file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border-0
                  file:text-xs file:font-medium file:bg-blue-50 file:text-blue-700
                  dark:file:bg-blue-900/30 dark:file:text-blue-300
                  hover:file:bg-blue-100 dark:hover:file:bg-blue-900/50
                  border border-gray-300 dark:border-gray-600 rounded-lg px-1 py-1
                  bg-white dark:bg-gray-700"
              />
              <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{field.hint}</p>
            </div>
          ))}

          {error && (
            <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 px-4 py-3">
              <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
            </div>
          )}

          {result !== null && (
            <div className="rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 px-4 py-3">
              <p className="text-sm text-green-700 dark:text-green-400 font-medium">
                ✓ Successfully imported {result.toLocaleString()} employees!
              </p>
            </div>
          )}

          <div className="flex justify-end gap-3 pt-1">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg
                text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              {result !== null ? 'Close' : 'Cancel'}
            </button>
            {result === null && (
              <button
                type="submit"
                disabled={importing || !allSelected}
                className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700
                  disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {importing && (
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                )}
                {importing ? 'Importing…' : 'Import'}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  )
}
