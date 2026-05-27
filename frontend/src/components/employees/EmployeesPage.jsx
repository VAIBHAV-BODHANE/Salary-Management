import { useState } from 'react'
import { useEmployees } from '../../hooks/useEmployees'
import { deleteEmployee } from '../../api/client'
import EmployeeTable from './EmployeeTable'
import SearchBar from './SearchBar'
import Pagination from './Pagination'
import EmployeeModal from './EmployeeModal'
import ImportModal from './ImportModal'

export default function EmployeesPage() {
  const { employees, total, page, pages, per_page, loading, error, setPage, search, setSearch, refetch } =
    useEmployees()
  const [modal, setModal] = useState({ open: false, mode: 'add', employee: null })
  const [importOpen, setImportOpen] = useState(false)

  const openAdd = () => setModal({ open: true, mode: 'add', employee: null })
  const openEdit = (emp) => setModal({ open: true, mode: 'edit', employee: emp })
  const closeModal = () => setModal((m) => ({ ...m, open: false }))

  const handleDelete = async (emp) => {
    if (!window.confirm(`Delete ${emp.full_name}?`)) return
    try {
      await deleteEmployee(emp.empid)
      refetch()
    } catch (e) {
      alert(`Failed to delete: ${e.message}`)
    }
  }

  return (
    <div>
      <div className="flex items-center gap-3 mb-4">
        <div className="flex-1">
          <SearchBar value={search} onChange={setSearch} />
        </div>
        <button
          onClick={() => setImportOpen(true)}
          className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 whitespace-nowrap flex items-center gap-1.5"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Import
        </button>
        <button
          onClick={openAdd}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 whitespace-nowrap"
        >
          + Add Employee
        </button>
      </div>

      {error && <p className="text-sm text-red-600 dark:text-red-400 mb-4">{error}</p>}

      <EmployeeTable employees={employees} loading={loading} onEdit={openEdit} onDelete={handleDelete} />

      <Pagination page={page} pages={pages} total={total} perPage={per_page} onPageChange={setPage} />

      {modal.open && (
        <EmployeeModal
          mode={modal.mode}
          employee={modal.employee}
          onClose={closeModal}
          onSaved={refetch}
        />
      )}

      {importOpen && (
        <ImportModal
          onClose={() => setImportOpen(false)}
          onImported={refetch}
        />
      )}
    </div>
  )
}
