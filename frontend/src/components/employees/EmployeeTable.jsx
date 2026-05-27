const fmtSalary = (n) =>
  Number(n).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })

const HEADERS = ['ID', 'Full Name', 'Job Title', 'Country', 'Salary', 'Date of Joining', 'Date of Birth', 'Actions']

export default function EmployeeTable({ employees, loading, onEdit, onDelete }) {
  if (loading) {
    return (
      <div className="flex items-center justify-center h-48 text-gray-400 dark:text-gray-500 border border-gray-200 dark:border-gray-700 rounded-lg">
        Loading…
      </div>
    )
  }

  if (!employees.length) {
    return (
      <div className="flex items-center justify-center h-48 text-gray-400 dark:text-gray-500 border border-gray-200 dark:border-gray-700 rounded-lg">
        No employees found.
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 text-sm">
        <thead className="bg-gray-50 dark:bg-gray-800">
          <tr>
            {HEADERS.map((h) => (
              <th
                key={h}
                className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide whitespace-nowrap"
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 dark:divide-gray-700 bg-white dark:bg-gray-900">
          {employees.map((emp) => (
            <tr key={emp.empid} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <td className="px-4 py-3 text-gray-400 dark:text-gray-500">{emp.empid}</td>
              <td className="px-4 py-3 font-medium text-gray-900 dark:text-gray-100">{emp.full_name}</td>
              <td className="px-4 py-3 text-gray-700 dark:text-gray-300">{emp.job_title}</td>
              <td className="px-4 py-3 text-gray-700 dark:text-gray-300">{emp.country}</td>
              <td className="px-4 py-3 font-mono text-gray-700 dark:text-gray-300">{fmtSalary(emp.salary)}</td>
              <td className="px-4 py-3 text-gray-600 dark:text-gray-400">{emp.doj}</td>
              <td className="px-4 py-3 text-gray-600 dark:text-gray-400">{emp.dob}</td>
              <td className="px-4 py-3">
                <div className="flex gap-2">
                  <button
                    onClick={() => onEdit(emp)}
                    className="px-2.5 py-1 text-xs bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-700 rounded hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => onDelete(emp)}
                    className="px-2.5 py-1 text-xs bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-700 rounded hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
