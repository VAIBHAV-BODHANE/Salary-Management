const fmtSalary = (n) =>
  Number(n).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })

export default function TopEarnersTable({ data }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
      <h3 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Top 10 Earners</h3>
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            <th className="pb-3 pr-3 w-8">#</th>
            <th className="pb-3 pr-3">Name</th>
            <th className="pb-3 pr-3">Job Title</th>
            <th className="pb-3 pr-3">Country</th>
            <th className="pb-3 text-right">Salary</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
          {data.map((e, i) => (
            <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td className="py-2.5 pr-3 text-gray-400 dark:text-gray-500 font-mono">{i + 1}</td>
              <td className="py-2.5 pr-3 font-medium text-gray-900 dark:text-gray-100">{e.full_name}</td>
              <td className="py-2.5 pr-3 text-gray-600 dark:text-gray-400">{e.job_title}</td>
              <td className="py-2.5 pr-3 text-gray-600 dark:text-gray-400">{e.country}</td>
              <td className="py-2.5 text-right font-mono font-semibold text-emerald-700 dark:text-emerald-400">
                {fmtSalary(e.salary)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
