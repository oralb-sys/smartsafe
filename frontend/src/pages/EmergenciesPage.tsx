import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {
  getEmergencies,
} from '../services/api'

import type {
  EmergencyListItem,
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


function EmergenciesPage() {
  const navigate = useNavigate()

  const [
    emergencies,
    setEmergencies,
  ] = useState<EmergencyListItem[]>([])

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')


  useEffect(() => {
    async function loadEmergencies() {
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
          await getEmergencies(
            token,
          )

        setEmergencies(data)
      } catch {
        setError(
          'No se pudieron cargar las emergencias.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadEmergencies()
  }, [navigate])


  return (
    <main className="reports-page">
      <section className="reports-card">
        <div className="reports-header">
          <div>
            <h1>
              Emergencias SmartSOS
            </h1>

            <p>
              Alertas registradas por los ciudadanos
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              navigate('/dashboard')
            }
          >
            Volver
          </button>
        </div>


        {loading && (
          <p>
            Cargando emergencias...
          </p>
        )}


        {error && (
          <p className="form-error">
            {error}
          </p>
        )}


        {!loading &&
          !error &&
          emergencies.length === 0 && (
            <div className="empty-state">
              <h2>
                No hay emergencias registradas
              </h2>

              <p>
                Las nuevas alertas SOS aparecerán aquí.
              </p>
            </div>
          )}


        {!loading &&
          emergencies.length > 0 && (
            <div className="report-list">
              {emergencies.map(
                (emergency) => (
                  <article
                    key={
                      emergency.id
                    }
                    className="report-item emergency-item"
                  >
                    <div className="report-item-main">
                      <div>
                        <span className="emergency-label">
                          SmartSOS
                        </span>

                        <h2>
                          Emergencia
                        </h2>

                        <p>
                          {
                            formatDate(
                              emergency.created_at,
                            )
                          }
                        </p>
                      </div>

                      <span
                        className="report-status"
                      >
                        {
                          emergency.status
                        }
                      </span>
                    </div>

                    <div className="emergency-location-summary">
                      {emergency.latitude !==
                        null &&
                      emergency.longitude !==
                        null ? (
                        <p>
                          Ubicación registrada:
                          {' '}
                          {emergency.latitude},
                          {' '}
                          {emergency.longitude}
                        </p>
                      ) : (
                        <p>
                          Ubicación pendiente
                        </p>
                      )}
                    </div>

                    <div className="report-item-actions">
                      <button
                        type="button"
                        className="report-detail-button"
                        onClick={() =>
                          navigate(
                            `/emergencies/${emergency.id}`,
                          )
                        }
                      >
                        Ver detalle
                      </button>
                    </div>
                  </article>
                ),
              )}
            </div>
          )}
      </section>
    </main>
  )
}

export default EmergenciesPage