import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { useDark } from '../../hooks/useDark'

const fmtAxis = (v) => `$${(v / 1000).toFixed(0)}k`
const fmtTip = (v) => `$${Number(v).toLocaleString()}`

export default function SalaryByCountryChart({ data }) {
  const dark = useDark()
  const tickColor = dark ? '#9ca3af' : '#6b7280'
  const gridColor = dark ? '#374151' : undefined
  const tooltipStyle = dark
    ? { backgroundColor: '#1f2937', border: '1px solid #374151', color: '#f9fafb' }
    : {}

  const chartData = data.map((d) => ({
    country: d.country,
    Min: Math.round(d.min),
    Avg: Math.round(d.avg),
    Max: Math.round(d.max),
  }))

  const minWidth = Math.max(640, data.length * 70)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
      <h3 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Salary by Country — Min / Avg / Max</h3>
      <div className="overflow-x-auto">
        <div style={{ minWidth }}>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 70 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
              <XAxis dataKey="country" angle={-40} textAnchor="end" tick={{ fontSize: 11, fill: tickColor }} interval={0} />
              <YAxis tickFormatter={fmtAxis} tick={{ fontSize: 11, fill: tickColor }} />
              <Tooltip formatter={fmtTip} contentStyle={tooltipStyle} />
              <Legend verticalAlign="top" wrapperStyle={{ color: tickColor }} />
              <Bar dataKey="Min" fill="#93c5fd" />
              <Bar dataKey="Avg" fill="#3b82f6" />
              <Bar dataKey="Max" fill="#1d4ed8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
