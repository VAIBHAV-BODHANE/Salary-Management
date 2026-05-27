import { useState, useMemo } from 'react'

const fmtCurrency = (n) =>
  Number(n).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })

export default function SalaryByTitleTable({ data }) {
  const [countryFilter, setCountryFilter] = useState('')
  const [sortKey, setSortKey] = useState('avg')
  const [sortDir, setSortDir] = useState('desc')

  const countries = useMemo(() => [...new Set(data.map((d) => d.country))].sort(), [data])

  const filtered = useMemo(() => {
    const rows = countryFilter ? data.filter((d) => d.country === countryFilter) : data
    return [...rows].sort((a, b) =>
      sortDir === 'desc' ? b[sortKey] - a[sortKey] : a[sortKey] - b[sortKey],
    )
  }, [data, countryFilter, sortKey, sortDir])

  const toggleSort = (key) => {
    if (sortKey === key) setSortDir((d) => (d === 'desc' ? 'asc' : 'desc'))
    else { setSortKey(key); setSortDir('desc') }
  }

  const sortIcon = (key) => (sortKey === key ? (sortDir === 'desc' ? ' ↓' : ' ↑') : '')

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-800 dark:text-gray-100">Avg Salary by Job Title × Country</h3>
        <select
          value={countryFilter}
          onChange={(e) => setCountryFilter(e.target.value)}
          className="text-sm border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5
            bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
            focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Countries</option>
          {countries.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <div className="max-h-96 overflow-y-auto rounded border border-gray-100 dark:border-gray-700">
        <table className="min-w-full text-sm">
          <thead className="sticky top-0 bg-gray-50 dark:bg-gray-700 z-10">
            <tr className="text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              <th className="px-4 py-3 pr-4">Job Title</th>
              <th className="px-4 py-3 pr-4">Country</th>
              <th
                className="px-4 py-3 pr-4 cursor-pointer select-none hover:text-gray-800 dark:hover:text-gray-200"
                onClick={() => toggleSort('avg')}
              >
                Avg Salary{sortIcon('avg')}
              </th>
              <th
                className="px-4 py-3 cursor-pointer select-none hover:text-gray-800 dark:hover:text-gray-200"
                onClick={() => toggleSort('count')}
              >
                Headcount{sortIcon('count')}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700 bg-white dark:bg-gray-800">
            {filtered.map((row, i) => (
              <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td className="px-4 py-2.5 font-medium text-gray-900 dark:text-gray-100">{row.job_title}</td>
                <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{row.country}</td>
                <td className="px-4 py-2.5 font-mono text-blue-700 dark:text-blue-400">{fmtCurrency(row.avg)}</td>
                <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{row.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">{filtered.length} combinations shown</p>
    </div>
  )
}
