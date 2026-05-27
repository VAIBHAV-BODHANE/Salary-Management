import { useState, useEffect, useCallback, useRef } from 'react'
import { getEmployees } from '../api/client'

const EMPTY = { employees: [], total: 0, page: 1, per_page: 50, pages: 1 }

export function useEmployees() {
  const [page, setPage] = useState(1)
  const [perPage] = useState(50)
  const [search, setSearch] = useState('')
  const [pendingSearch, setPendingSearch] = useState('')
  const [data, setData] = useState(EMPTY)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const debounceRef = useRef(null)

  const fetchEmployees = useCallback(
    async (p, s) => {
      setLoading(true)
      setError(null)
      try {
        const result = await getEmployees({ page: p, perPage, search: s })
        setData(result)
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    },
    [perPage],
  )

  useEffect(() => {
    fetchEmployees(page, search)
  }, [page]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleSearch = useCallback(
    (value) => {
      setPendingSearch(value)
      clearTimeout(debounceRef.current)
      debounceRef.current = setTimeout(() => {
        setSearch(value)
        setPage(1)
        fetchEmployees(1, value)
      }, 300)
    },
    [fetchEmployees],
  )

  const refetch = useCallback(() => {
    fetchEmployees(page, search)
  }, [page, search, fetchEmployees])

  const handlePageChange = useCallback(
    (p) => {
      setPage(p)
    },
    [],
  )

  return {
    ...data,
    loading,
    error,
    page,
    setPage: handlePageChange,
    search: pendingSearch,
    setSearch: handleSearch,
    refetch,
  }
}
