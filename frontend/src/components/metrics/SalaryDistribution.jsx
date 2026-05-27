import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useDark } from '../../hooks/useDark'

export default function SalaryDistribution({ data }) {
  const dark = useDark()
  const tickColor = dark ? '#9ca3af' : '#6b7280'
  const gridColor = dark ? '#374151' : undefined
  const tooltipStyle = dark
    ? { backgroundColor: '#1f2937', border: '1px solid #374151', color: '#f9fafb' }
    : {}

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
      <h3 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Salary Distribution</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
          <XAxis dataKey="bucket" tick={{ fontSize: 12, fill: tickColor }} />
          <YAxis tick={{ fontSize: 12, fill: tickColor }} />
          <Tooltip
            formatter={(v) => [v.toLocaleString(), 'Employees']}
            labelFormatter={(l) => `Salary range: ${l}`}
            contentStyle={tooltipStyle}
          />
          <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} name="Employees" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
