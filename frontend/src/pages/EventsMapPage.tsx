import {
  useEffect,
  useState,
} from 'react'

import {
  useNavigate,
} from 'react-router-dom'

import EventsMap from '../components/EventsMap'

import {
  getUrbanEvents,
} from '../services/api'

import type {
  UrbanEvent,
} from '../services/api'

import './EventsMapPage.css'


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


function EventsMapPage() {
  const navigate =
    useNavigate()

  const [
    events,
    setEvents,
  ] = useState<UrbanEvent[]>([])

  const [
    selectedEvent,
    setSelectedEvent,
  ] = useState<UrbanEvent | null>(
    null,
  )

  const [
    loading,
    setLoading,
  ] = useState(true)

  const [
    error,
    setError,
  ] = useState('')


  useEffect(() => {
    async function loadEvents() {
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
          await getUrbanEvents(
            token,
          )

        setEvents(data)
      } catch {
        setError(
          'No se pudieron cargar los eventos del mapa.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadEvents()
  }, [
    navigate,
  ])


  const eventsWithLocation =
    events.filter(
      (event) =>
        event.latitude !== null &&
        event.longitude !== null,
    )


  return (
    <main className="events-map-page">
      <section className="events-map-card">

        <div className="events-map-header">
          <div>
            <h1>
              Mapa de eventos
            </h1>

            <p>
              Visualización conjunta de
              SmartReport y SmartSOS
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              navigate(
                '/dashboard',
              )
            }
          >
            Volver
          </button>
        </div>


        <div className="events-map-legend">
          <span>
            <i className="legend-dot legend-report" />
            SmartReport
          </span>

          <span>
            <i className="legend-dot legend-sos" />
            SmartSOS
          </span>
        </div>


        {loading && (
          <p>
            Cargando eventos...
          </p>
        )}


        {error && (
          <p className="form-error">
            {error}
          </p>
        )}


        {!loading &&
          !error && (
            <>
              <div className="events-map-summary">
                <strong>
                  {
                    eventsWithLocation.length
                  }
                </strong>
                {' '}
                eventos con ubicación
              </div>

              <div className="events-map-layout">
                <div className="events-map-main">
                  <EventsMap
                    events={events}
                    onSelectEvent={
                      setSelectedEvent
                    }
                  />
                </div>

                <aside className="event-selection-panel">
                  {!selectedEvent && (
                    <div className="event-selection-empty">
                      <h2>
                        Selecciona un evento
                      </h2>

                      <p>
                        Haz clic sobre un
                        marcador para consultar
                        su información básica.
                      </p>
                    </div>
                  )}

                  {selectedEvent && (
                    <>
                      <span
                        className={
                          selectedEvent.source ===
                          'SMART_SOS'
                            ? 'event-source event-source-sos'
                            : 'event-source event-source-report'
                        }
                      >
                        {
                          selectedEvent.source ===
                          'SMART_SOS'
                            ? 'SmartSOS'
                            : 'SmartReport'
                        }
                      </span>

                      <h2>
                        {
                          selectedEvent.type
                        }
                      </h2>

                      <dl className="event-detail-list">
                        <div>
                          <dt>
                            Estado
                          </dt>

                          <dd>
                            {
                              selectedEvent.status
                            }
                          </dd>
                        </div>

                        <div>
                          <dt>
                            Fecha
                          </dt>

                          <dd>
                            {
                              formatDate(
                                selectedEvent.created_at,
                              )
                            }
                          </dd>
                        </div>

                        <div>
                          <dt>
                            Latitud
                          </dt>

                          <dd>
                            {
                              selectedEvent.latitude
                            }
                          </dd>
                        </div>

                        <div>
                          <dt>
                            Longitud
                          </dt>

                          <dd>
                            {
                              selectedEvent.longitude
                            }
                          </dd>
                        </div>
                      </dl>

                      {selectedEvent.description && (
                        <div className="event-description">
                          <strong>
                            Descripción
                          </strong>

                          <p>
                            {
                              selectedEvent.description
                            }
                          </p>
                        </div>
                      )}
                    </>
                  )}
                </aside>
              </div>
            </>
          )}

      </section>
    </main>
  )
}

export default EventsMapPage