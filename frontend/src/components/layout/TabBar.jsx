const TABS = [
  { id: 'metrics', label: 'Metrics' },
  { id: 'employees', label: 'Employees' },
]

export default function TabBar({ active, onChange }) {
  return (
    <nav className="flex gap-1 mt-4">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`px-5 py-2 text-sm font-medium rounded-t-md border-x border-t transition-colors
            ${
              active === tab.id
                ? 'bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-700 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  )
}
