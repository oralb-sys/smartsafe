import {
  useEffect,
  useState,
} from 'react'

import {
  useNavigate,
  useParams,
} from 'react-router-dom'

import LocationPicker from '../components/LocationPicker'

import {
  getEmergencyDetail,
} from '../services/api'

import type {
  EmergencyDetail,
} from '../services/api'


function formatDate(
  value: string,
) {
  return new Intl.DateTimeFormat(
    'es-PE',
    {
      dateStyle: 'medium',
      timeStyle: 'short',
    },
  ).format(
    new Date(value),
  )
}


function EmergencyDetailPage() {
  const navigate = useNavigate()

  const { id } = useParams()

  const [
    emergency,
    setEmergency,
  ] = useState<EmergencyDetail | null>(
    null,
  )

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')


  useEffect(() => {
    async function loadEmergency() {
      if (!id) {
        setError(
          'Identificador de emergencia inválido.',
        )
        setLoading(false)
        return
      }

      const token =
        localStorage.getItem(
          'smartsafe_token',
        )

      if (!token) {
        navigate('/login')
        return
      }

      try {
        const data =
          await getEmergencyDetail(
            id,
            token,
          )

        setEmergency(data)
      } catch {
        setError(
          'No se pudo cargar la emergencia.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadEmergency()
  }, [
    id,
    navigate,
  ])


  return (
    <main className="report-detail-page">
      <section className="report-detail-card">
        <div className="reports-header">
          <div>
            <h1>
              Detalle de emergencia
            </h1>

            <p>
              Información de la alerta SmartSOS
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              navigate('/emergencies')
            }
          >
            Volver
          </button>
        </div>


        {loading && (
          <p>
            Cargando emergencia...
          </p>
        )}


        {error && (
          <p className="form-error">
            {error}
          </p>
        )}


        {emergency && (
          <div className="emergency-detail-content">
            <div className="report-detail-grid">
              <div>
                <span className="detail-label">
                  Estado
                </span>

                <strong>
                  {emergency.status}
                </strong>
              </div>

              <div>
                <span className="detail-label">
                  Fecha
                </span>

                <strong>
                  {
                    formatDate(
                      emergency.created_at,
                    )
                  }
                </strong>
              </div>

              <div>
                <span className="detail-label">
                  ID de emergencia
                </span>

                <strong>
                  {emergency.id}
                </strong>
              </div>

              <div>
                <span className="detail-label">
                  ID ciudadano
                </span>

                <strong>
                  {emergency.user_id}
                </strong>
              </div>
            </div>


            {emergency.latitude !==
              null &&
            emergency.longitude !==
              null ? (
              <section className="emergency-map-section">
                <h2>
                  Ubicación de la emergencia
                </h2>

                <p>
                  Latitud:
                  {' '}
                  {emergency.latitude}
                  {' · '}
                  Longitud:
                  {' '}
                  {emergency.longitude}
                </p>

                <LocationPicker
                  latitude={
                    emergency.latitude
                  }
                  longitude={
                    emergency.longitude
                  }
                  onLocationChange={() => {
                    // Vista de consulta.
                  }}
                />
              </section>
            ) : (
              <div className="empty-state">
                <p>
                  Esta emergencia todavía
                  no tiene ubicación registrada.
                </p>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  )
}

export default EmergencyDetailPage