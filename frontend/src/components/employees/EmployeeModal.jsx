import { useState, useEffect } from 'react'
import { createEmployee, updateEmployee } from '../../api/client'

const EMPTY = { full_name: '', job_title: '', country: '', salary: '', doj: '', dob: '' }

const FIELDS = [
  { key: 'full_name', label: 'Full Name', type: 'text' },
  { key: 'job_title', label: 'Job Title', type: 'text' },
  { key: 'country', label: 'Country', type: 'text' },
  { key: 'salary', label: 'Salary (USD)', type: 'number', step: '0.01', min: '0' },
  { key: 'doj', label: 'Date of Joining', type: 'date' },
  { key: 'dob', label: 'Date of Birth', type: 'date' },
]

export default function EmployeeModal({ mode, employee, onClose, onSaved }) {
  const [form, setForm] = useState(EMPTY)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (mode === 'edit' && employee) {
      setForm({
        full_name: employee.full_name,
        job_title: employee.job_title,
        country: employee.country,
        salary: employee.salary,
        doj: employee.doj,
        dob: employee.dob,
      })
    } else {
      setForm(EMPTY)
    }
  }, [mode, employee])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setSaving(true)
    try {
      const data = { ...form, salary: parseFloat(form.salary) }
      if (mode === 'edit') {
        await updateEmployee(employee.empid, data)
      } else {
        await createEmployee(data)
      }
      onSaved()
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

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
          <h2 className="text-base font-semibold text-gray-900 dark:text-white">
            {mode === 'edit' ? 'Edit Employee' : 'Add Employee'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-4 space-y-4">
          {FIELDS.map((field) => (
            <div key={field.key}>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {field.label}
              </label>
              <input
                type={field.type}
                step={field.step}
                min={field.min}
                value={form[field.key]}
                onChange={(e) => setForm((f) => ({ ...f, [field.key]: e.target.value }))}
                required
                className="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 text-sm
                  bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                  focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}

          {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg
                text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Saving…' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
