import { useState, useEffect } from 'react'
import { getMetrics } from '../api/client'

export function useMetrics() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const controller = new AbortController()
    getMetrics(controller.signal)
      .then(setData)
      .catch((e) => { if (!controller.signal.aborted) setError(e.message) })
      .finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [])

  return { data, loading, error }
}
