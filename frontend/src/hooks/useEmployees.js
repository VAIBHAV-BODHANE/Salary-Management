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
  const [refetchCounter, setRefetchCounter] = useState(0)
  const debounceRef = useRef(null)

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError(null)
    getEmployees({ page, perPage, search }, controller.signal)
      .then((result) => setData(result))
      .catch((e) => { if (!controller.signal.aborted) setError(e.message) })
      .finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [page, search, perPage, refetchCounter])

  const handleSearch = useCallback((value) => {
    setPendingSearch(value)
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      setSearch(value)
      setPage(1)
    }, 300)
  }, [])

  const refetch = useCallback(() => setRefetchCounter((c) => c + 1), [])

  const handlePageChange = useCallback((p) => {
    setPage(p)
  }, [])

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
