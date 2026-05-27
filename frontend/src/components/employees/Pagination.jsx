export default function Pagination({ page, pages, total, perPage, onPageChange }) {
  const from = total === 0 ? 0 : (page - 1) * perPage + 1
  const to = Math.min(page * perPage, total)

  return (
    <div className="flex items-center justify-between mt-4 text-sm text-gray-600 dark:text-gray-400">
      <span>
        Showing {from.toLocaleString()}–{to.toLocaleString()} of {total.toLocaleString()} employees
      </span>
      <div className="flex items-center gap-2">
        <button
          onClick={() => onPageChange(1)}
          disabled={page <= 1}
          className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded disabled:opacity-40 hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          «
        </button>
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page <= 1}
          className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded disabled:opacity-40 hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          ← Prev
        </button>
        <span className="px-3">
          Page {page} of {pages}
        </span>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page >= pages}
          className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded disabled:opacity-40 hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          Next →
        </button>
        <button
          onClick={() => onPageChange(pages)}
          disabled={page >= pages}
          className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded disabled:opacity-40 hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          »
        </button>
      </div>
    </div>
  )
}
