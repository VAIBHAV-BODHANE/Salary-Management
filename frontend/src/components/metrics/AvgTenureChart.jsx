import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useDark } from '../../hooks/useDark'

export default function AvgTenureChart({ data }) {
  const dark = useDark()
  const tickColor = dark ? '#9ca3af' : '#6b7280'
  const gridColor = dark ? '#374151' : undefined
  const tooltipStyle = dark
    ? { backgroundColor: '#1f2937', border: '1px solid #374151', color: '#f9fafb' }
    : {}

  const chartData = data.map((d) => ({ country: d.country, Years: d.avg_tenure_years }))
  const minWidth = Math.max(640, data.length * 70)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
      <h3 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Avg Employee Tenure by Country (Years)</h3>
      <div className="overflow-x-auto">
        <div style={{ minWidth }}>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 70 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
              <XAxis dataKey="country" angle={-40} textAnchor="end" tick={{ fontSize: 11, fill: tickColor }} interval={0} />
              <YAxis tick={{ fontSize: 12, fill: tickColor }} unit="y" />
              <Tooltip formatter={(v) => [`${v} yrs`, 'Avg Tenure']} contentStyle={tooltipStyle} />
              <Bar dataKey="Years" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
