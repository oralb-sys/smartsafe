import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE_URL = 'http://localhost:8000/api/v1'

type ReportCategory =
  | 'POTHOLE'
  | 'WASTE'
  | 'STREET_LIGHT'
  | 'WATER_LEAK'

function ReportCreatePage() {
  const navigate = useNavigate()

  const [category, setCategory] = useState<ReportCategory>('POTHOLE')
  const [description, setDescription] = useState('')
  const [latitude, setLatitude] = useState('-13.5204')
  const [longitude, setLongitude] = useState('-71.9751')
  const [photoUrl, setPhotoUrl] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()

    setMessage('')
    setError('')
    setLoading(true)

    const token = localStorage.getItem('smartsafe_token')

    if (!token) {
      navigate('/login')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/reports`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          category,
          description: description || null,
          latitude: Number(latitude),
          longitude: Number(longitude),
          photo_url: photoUrl || null,
        }),
      })

      if (!response.ok) {
        throw new Error('No se pudo registrar la incidencia')
      }

      const data = await response.json()

      setMessage(
        `Incidencia registrada correctamente. Estado: ${data.status}`,
      )

      setDescription('')
      setPhotoUrl('')
    } catch {
      setError('No se pudo registrar la incidencia.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="report-page">
      <section className="report-card">
        <div className="report-header">
          <div>
            <h1>Registrar incidencia</h1>
            <p>SmartReport</p>
          </div>

          <button
            className="secondary-button"
            type="button"
            onClick={() => navigate('/dashboard')}
          >
            Volver
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <label htmlFor="category">Categoría</label>

          <select
            id="category"
            value={category}
            onChange={(event) =>
              setCategory(event.target.value as ReportCategory)
            }
          >
            <option value="POTHOLE">Bache</option>
            <option value="WASTE">Residuos</option>
            <option value="STREET_LIGHT">Alumbrado público</option>
            <option value="WATER_LEAK">Fuga de agua</option>
          </select>

          <label htmlFor="description">Descripción</label>

          <textarea
            id="description"
            rows={5}
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="Describe brevemente la incidencia"
          />

          <div className="coordinates-grid">
            <div>
              <label htmlFor="latitude">Latitud</label>
              <input
                id="latitude"
                type="number"
                step="any"
                value={latitude}
                onChange={(event) => setLatitude(event.target.value)}
                required
              />
            </div>

            <div>
              <label htmlFor="longitude">Longitud</label>
              <input
                id="longitude"
                type="number"
                step="any"
                value={longitude}
                onChange={(event) => setLongitude(event.target.value)}
                required
              />
            </div>
          </div>

          <label htmlFor="photoUrl">URL de fotografía (opcional)</label>

          <input
            id="photoUrl"
            type="url"
            value={photoUrl}
            onChange={(event) => setPhotoUrl(event.target.value)}
            placeholder="https://..."
          />

          {message && <p className="form-success">{message}</p>}
          {error && <p className="form-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? 'Registrando...' : 'Registrar incidencia'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default ReportCreatePage