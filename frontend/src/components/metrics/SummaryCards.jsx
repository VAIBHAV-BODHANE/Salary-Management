const fmtCurrency = (n) =>
  Number(n).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })

const COLOR = {
  blue:   'bg-blue-50   dark:bg-blue-900/30   border-blue-200   dark:border-blue-700   text-blue-900   dark:text-blue-200',
  green:  'bg-green-50  dark:bg-green-900/30  border-green-200  dark:border-green-700  text-green-900  dark:text-green-200',
  purple: 'bg-purple-50 dark:bg-purple-900/30 border-purple-200 dark:border-purple-700 text-purple-900 dark:text-purple-200',
  amber:  'bg-amber-50  dark:bg-amber-900/30  border-amber-200  dark:border-amber-700  text-amber-900  dark:text-amber-200',
  teal:   'bg-teal-50   dark:bg-teal-900/30   border-teal-200   dark:border-teal-700   text-teal-900   dark:text-teal-200',
  rose:   'bg-rose-50   dark:bg-rose-900/30   border-rose-200   dark:border-rose-700   text-rose-900   dark:text-rose-200',
}

export default function SummaryCards({ summary }) {
  const cards = [
    { label: 'Total Employees',        value: summary.total_employees?.toLocaleString(), color: 'blue' },
    { label: 'Countries',              value: summary.total_countries,                   color: 'green' },
    { label: 'Overall Avg Salary',     value: fmtCurrency(summary.overall_avg_salary),  color: 'purple' },
    { label: 'Highest Salary',         value: fmtCurrency(summary.highest_salary),      color: 'amber' },
    { label: 'Most Common Role',       value: summary.most_common_title,                color: 'teal' },
    { label: 'Highest-Paying Country', value: summary.highest_paying_country,           color: 'rose' },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
      {cards.map((c) => (
        <div key={c.label} className={`rounded-xl border p-4 ${COLOR[c.color]}`}>
          <p className="text-xs font-medium opacity-60 uppercase tracking-wide leading-tight">{c.label}</p>
          <p className="text-lg font-bold mt-2 leading-tight">{c.value ?? '—'}</p>
        </div>
      ))}
    </div>
  )
}
