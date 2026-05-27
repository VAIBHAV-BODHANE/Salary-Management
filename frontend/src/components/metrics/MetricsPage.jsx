import { useMetrics } from '../../hooks/useMetrics'
import SummaryCards from './SummaryCards'
import SalaryByCountryChart from './SalaryByCountryChart'
import SalaryDistribution from './SalaryDistribution'
import HeadcountChart from './HeadcountChart'
import TopEarnersTable from './TopEarnersTable'
import SalaryByTitleTable from './SalaryByTitleTable'
import AvgTenureChart from './AvgTenureChart'

export default function MetricsPage() {
  const { data, loading, error } = useMetrics()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400 dark:text-gray-500">
        Loading metrics…
      </div>
    )
  }

  if (error) {
    return <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
  }

  if (!data || !data.summary.total_employees) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400 dark:text-gray-500 flex-col gap-2">
        <p className="text-lg">No data yet</p>
        <p className="text-sm">Switch to the Employees tab to add or import employees.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <SummaryCards summary={data.summary} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SalaryByCountryChart data={data.salary_by_country} />
        <SalaryDistribution data={data.salary_distribution} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HeadcountChart data={data.headcount_by_title} />
        <TopEarnersTable data={data.top_earners} />
      </div>

      <SalaryByTitleTable data={data.salary_by_title_country} />

      <AvgTenureChart data={data.avg_tenure_by_country} />
    </div>
  )
}
