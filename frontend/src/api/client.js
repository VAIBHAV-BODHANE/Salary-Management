const BASE = '/api'

async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }))
    throw new Error(err.error || res.statusText)
  }
  return res.json()
}

export function getEmployees({ page = 1, perPage = 50, search = '' } = {}, signal) {
  const params = new URLSearchParams({ page, per_page: perPage })
  if (search) params.set('search', search)
  return apiFetch(`/employees?${params}`, { signal })
}

export function createEmployee(data) {
  return apiFetch('/employees', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export function updateEmployee(id, data) {
  return apiFetch(`/employees/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export function deleteEmployee(id) {
  return apiFetch(`/employees/${id}`, { method: 'DELETE' })
}

export function getMetrics(signal) {
  return apiFetch('/employees/metrics', { signal })
}
