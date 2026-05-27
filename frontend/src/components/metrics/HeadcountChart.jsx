import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useDark } from '../../hooks/useDark'

export default function HeadcountChart({ data }) {
  const dark = useDark()
  const tickColor = dark ? '#9ca3af' : '#6b7280'
  const gridColor = dark ? '#374151' : undefined
  const tooltipStyle = dark
    ? { backgroundColor: '#1f2937', border: '1px solid #374151', color: '#f9fafb' }
    : {}

  const top15 = data.slice(0, 15)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
      <h3 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Headcount by Job Title (Top 15)</h3>
      <ResponsiveContainer width="100%" height={340}>
        <BarChart data={top15} layout="vertical" margin={{ top: 5, right: 30, left: 150, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
          <XAxis type="number" tick={{ fontSize: 11, fill: tickColor }} />
          <YAxis dataKey="job_title" type="category" width={145} tick={{ fontSize: 11, fill: tickColor }} />
          <Tooltip formatter={(v) => [v.toLocaleString(), 'Employees']} contentStyle={tooltipStyle} />
          <Bar dataKey="count" fill="#10b981" radius={[0, 4, 4, 0]} name="Employees" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
