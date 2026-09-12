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
  const [photo, setPhoto] = useState<File | null>(null)
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
    setLoading(false)
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
        photo_url: null,
      }),
    })

    if (!response.ok) {
      throw new Error('REPORT_CREATE_FAILED')
    }

    const data = await response.json()

    if (photo) {
      const formData = new FormData()
      formData.append('photo', photo)

      const photoResponse = await fetch(
        `${API_BASE_URL}/reports/${data.id}/photo`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        },
      )

      if (!photoResponse.ok) {
        setError(
          'La incidencia fue registrada, pero no se pudo adjuntar la fotografía.',
        )
        return
      }
    }

    setMessage(
      `Incidencia registrada correctamente. Estado: ${data.status}`,
    )

    setDescription('')
    setPhoto(null)
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

          <label htmlFor="photo">
  Fotografía (opcional)
</label>

<input
  id="photo"
  type="file"
  accept="image/*"
  capture="environment"
  onChange={(event) => {
    const selectedFile =
      event.target.files?.[0] ?? null

    if (
      selectedFile &&
      selectedFile.size > 5 * 1024 * 1024
    ) {
      setError(
        'La fotografía no puede superar los 5 MB.',
      )
      event.target.value = ''
      setPhoto(null)
      return
    }

    setError('')
    setPhoto(selectedFile)
  }}
/>

<p className="photo-help">
  En móvil puedes tomar una foto con la cámara.
  También puedes seleccionar una imagen existente.
  Tamaño máximo: 5 MB.
</p>

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